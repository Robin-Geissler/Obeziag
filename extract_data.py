import lxml.html
import datetime
import re


# Data extracted from Moodle
class Processed_Section:
    def __init__(self, date, calender_week, assignments, scripts, other):
        self.date = date
        self.kw = calender_week
        self.assignments = assignments
        self.scripts = scripts
        self.other = other

    def print(self):
        print(self.date, '  KW:', self.kw)

        print('Assignments:')
        for ass in self.assignments:
            print(ass)

        print('Scripts:')
        for scr in self.scripts:
            print(scr)

        print('Others:')
        for oth in self.other:
            print(oth)

        print('\n')


filename = "ana_html.txt"
file_open = open(filename, "r")
html = file_open.read()

root = lxml.html.fromstring(html.encode('utf-8'))

############################################################################

month_dict = {'Januar': 1, 'Februar': 2, 'März': 3, 'April': 4, 'Mai': 5, 'Juni': 6, 'Juli': 7, 'August': 8,
              'September': 9, 'Oktober': 10, 'November': 11, 'Dezember': 12,
              'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
              'September': 9, 'October': 10, 'November': 11, 'December': 12,
              'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
              'Nov': 11, 'Dec': 12}


def parseDateToKW(date):
    try:
        day = int((re.findall(r'\d+', date))[0])

        month_str = re.findall(r'[a-zA-Z]+', date)
        month = int(month_dict[month_str[0]])

        year = 2019  # ToDo: Hardcoded-change
        kw = datetime.date(year, month, day).strftime("%V")
        return kw
    except:
        return 0  # ToDo: Problem wenn Datum nicht vorhanden


def removeUmlaut(word):
    word = word.replace('ö', 'oe')
    word = word.replace('ä', 'ae')
    word = word.replace('ü', 'ue')

    word = word.replace('Ö', 'Oe')
    word = word.replace('Ä', 'Ae')
    word = word.replace('Ü', 'Ue')

    word = word.replace('ß', 'ss')
    return word




def getData(html, course):
    root = lxml.html.fromstring(html.encode('utf-8'))

    sect = root.find_class('section main')

    # Section Allgemeines entfernen
    sect.pop(0)

    sections = []

    # all sections
    for sec in sect:
        date = sec[0].text_content()
        kw = parseDateToKW(date)

        assignments = []
        scripts = []
        others = []

        for docs in sec.find_class('activityinstance'):

            #Spezialfälle falls man nicht auf link zugreifen kann
            if(not(docs.xpath("a"))):
                continue

            link = (docs.xpath("a"))[0].get('href')
            name_of_file = docs.find_class('instancename')[0].text

            nof = removeUmlaut(name_of_file)

            if re.match(course['pattern_script'], name_of_file):
                scripts.append(((nof, link)))

            elif re.match(course['pattern_assignment'], name_of_file):
                assignments.append((nof, link))

            # Alle anderen Links und auch splashes
            else:
                others.append((nof, link))

        if (not assignments) and (not scripts) and (not others):
            continue
        else:
            sections.append(Processed_Section(date, kw, assignments, scripts, others))

    return sections


def getData_splash(html, course):

    data = []




    return data
