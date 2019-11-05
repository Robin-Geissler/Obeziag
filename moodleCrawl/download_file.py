import os
import re
import requests
import sys
import lxml.html


def prepairForFilename(word, org_filename):
    splitt = org_filename.split('.')
    ext = splitt[len(splitt)-1]

    word = word.replace('.', ' ')
    word = word.replace('_', ' ')
    word = word.replace(':', ' ')
    word = word.replace('/', ' ')
    word = re.sub(' +', ' ', word)
    word = word.rstrip()
    word = word.replace(' ', '_')
    return word + '.' + ext


def download(url_data, session, course, folder):
    # ToDo: basepath hardcoded sollte von course kommen
    basepath = os.path.dirname(os.path.realpath(__file__))      #ermittelt basepath von aktuellen Speicherort des Projectes
    # basepath = '/Users/maximilianpalmer/OneDrive - tum.de/4.Semester'

    url = url_data[1]

    ################### Cheack if URL aviable ###################
    res = session.head(url, allow_redirects=True)

    if not res.ok:
        return None

    print(res.headers)

    if 'text/html' in res.headers['Content-Type']:
        #ToDo: Splash
        return 'Todo'

    else:
        ################### Get Filename ###################
        # Get Name from PDF
        res = re.search(r'filename="(.*)"', res.headers['content-disposition'])

        if not res:
            return None

        org_filename = res.group(1)
        #print(org_filename)

        # Use name which is displayed in moodle
        filename = url_data[0]
        filename = prepairForFilename(filename, org_filename)
        #print(filename)

        ################### Generate Path ###################
        dirpath = os.path.join(basepath, course['name'], folder)
        filepath = os.path.join(dirpath, filename)

        # Check if Path exists
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        # Check if File exists
        if os.path.isfile(filepath):
            #    if folder != 'scripts' or size <= os.path.getsize(filepath):
            return ''

        ################ Download File ################
        res = session.get(url, stream=True)
        if not res.ok:
            return None

        with open(filepath, 'wb') as f:
            for chunk in res:
                f.write(chunk)

        return filename


def manage_download(course, data, session):
    newFiles = []

    #d = data[4]
    for d in data:
        for d_a in d.assignments:
            returnValue = download(d_a, session, course, '2_assignments')

            if returnValue is None:
                print("Big Problem: URL is wrong")
            elif returnValue != '':
                newFiles.append(returnValue)

        for d_s in d.scripts:
            returnValue = download(d_s, session, course, '1_lecture')

            if returnValue is None:
                print("Big Problem: URL is wrong")
            elif returnValue != '':
                newFiles.append(returnValue)


    print(newFiles)
