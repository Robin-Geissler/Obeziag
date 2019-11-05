#!/bin/python3

"""
args: <USER> <PASSWORD> [<PATH>]

<PATH> will be created if it does not exist yet.
Directory structure: <PATH>/{COURSE_NAME}(/{SHEET_NAME})/[{FILE_NAME}]

"""

import os
import requests
import sys
import lxml.html

sys.path.append("moodleCrawl")

import download_file
import extract_moodle_data
import dataFunctions

#Bei Pattern muss genau angegeben werden kann auch mit oder benutzt werden
COURSES = [
    # {
    #     'name': 'analysis',
    #     'id': '43628',
    #     'splash': False,
    #     'basepath': '',
    #     'pattern_assignment': r'Übungsblatt',
    #     'pattern_script': r'Skript',
    # },
    # {
    #   'name': 'SMS',
    #    'id': '46016',
    #    'splash': True,
    #    'basepath': '',
    #    'pattern_assignment': r'Übungsblatt',
    #    'pattern_script': r'Kapitel.*',
    # },
    {
        'name': 'NumProg',
        'id': '45799',
        'splash': False,
        'basepath': '',
        'pattern_assignment': r'Übungsblatt.*|Lösung.* ',
        'pattern_script': r'Vorlesung.*',
    }
]

MOODLE_HOST = 'https://www.moodle.tum.de'
TUMIDP_HOST = 'https://tumidp.lrz.de'
SHIBBOLETH = 'Shibboleth.sso/Login?providerId=https%3A%2F%2Ftumidp.lrz.de%2Fidp%2Fshibboleth&target=https%3A%2F%2Fwww.moodle.tum.de%2Fauth%2Fshibboleth%2Findex.php'

######################## Input verarbeiten ########################
if (len(sys.argv) < 3):
    print("args: <USER> <PASSWORD> [<PATH>]")
    sys.stdout.flush()
    exit(None)


USER = dataFunctions.read_login_data()[0]
PASSWORD = dataFunctions.read_login_data()[1]

if (len(sys.argv) > 3):
    basepath = sys.argv[3]
else:
    basepath = os.path.dirname(os.path.realpath(__file__))


########################################################################

######################### Check Internet connection ########################
try:
    requests.get('https://www.google.com', timeout=0.5)
except:
    print('No internet connection')
    quit()


################################################################################################


def get(path):
    return session.get('{}/{}'.format(MOODLE_HOST, path))


######################### login with user and passwort -> generate Session ########################
session = requests.Session()


def login():
    html = get(SHIBBOLETH).text
    root = lxml.html.fromstring(html.encode('utf-8'))

    post_url = root.xpath('//form/@action')[0]
    post_data = {
        'j_username': USER,
        'j_password': PASSWORD,
        'donotcache': 1,
        '_eventId_proceed': ''
    }

    html = session.post('{}/{}'.format(TUMIDP_HOST, post_url), data=post_data).text
    root = lxml.html.fromstring(html.encode('utf-8'))

    post_url = root.xpath('//form/@action')[0]
    post_relay_state = root.xpath('//input[@name="RelayState"]/@value')
    post_saml_response = root.xpath('//input[@name="SAMLResponse"]/@value')
    post_data = {
        'RelayState': post_relay_state,
        'SAMLResponse': post_saml_response
    }

    session.post(post_url, data=post_data)


print('Login in Moodle')
login()
print('Login was succesfull\n')

################################################################################################

###############################################################
sys.stdout.flush()
##################################################################
# Iterate through courses
for course in COURSES:
    html = get('course/view.php?id={}'.format(course['id'])).text

    #Return a Array of all sections from the course
    print('Colllect Data ...')
    data = extract_moodle_data.getData(html, course)
    print('Finish with collecting Data\n')

    print('-------->', course['name'], '<--------')
    for d in data:
        d.print()

    print('\n\n')

    print('Start downloading Files ...')
    download_file.manage_download(course, data, session)
    print('Finsh downloading Files\n')

