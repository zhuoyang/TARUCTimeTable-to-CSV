import sys
import urllib.request
import pathlib
import datetime
import csv
import os
from bs4 import BeautifulSoup

cwd = os.path.dirname(os.path.abspath(__file__))
page = urllib.request.urlopen("file:///" + cwd + "/" + sys.argv[1])
soup = BeautifulSoup(page, 'html5lib')

allTable = soup.findAll('table', {'id': 'simple-table'})
table = allTable[1].find('tbody').findAll('tr')

semDate = soup.find('div', {'class': 'form-group'}).findAll('label')[1].contents[2].split(" ")[4]
semDateTime = datetime.datetime.strptime(semDate, "%Y-%m-%d")

dayDict = {
    "Mon": semDateTime,
    "Tue": semDateTime + datetime.timedelta(days=1),
    "Wed": semDateTime + datetime.timedelta(days=2),
    "Thu": semDateTime + datetime.timedelta(days=3),
    "Fri": semDateTime + datetime.timedelta(days=4),
    "Sat": semDateTime + datetime.timedelta(days=5),
    "Sun": semDateTime + datetime.timedelta(days=6)
}

class Lesson:
    def __init__(self, day, starttime, endtime, venue, lecturer, type):
        self.day = day
        self.starttime = starttime
        self.endtime = endtime
        self.venue = venue
        self.lecturer = lecturer
        self.type = type


class Subject:

    def __init__(self, name):
        self.name = name
        self.lesson = []


i = -1
subjects = []
for row in table:
    child = row.findAll('td')
    if len(child) == 5:
        i += 1
        name = list(child[1].stripped_strings)[2]
        subject = Subject(name)
        subjects.append(subject)
        if len(list(child[2].stripped_strings)) == 3:
            continue
        string = list(child[2].stripped_strings)[0].split(" ")
        venue = list(child[3].stripped_strings)[0].split(",")[0]
        lecturer = list(child[4].stripped_strings)[0]
    else:
        if len(list(child[0].stripped_strings)) == 3:
            continue
        string = list(child[0].stripped_strings)[0].split(" ")
        venue = list(child[1].stripped_strings)[0].split(",")[0]
        lecturer = list(child[2].stripped_strings)[0]
    test = list(child[2].stripped_strings)
    lesson = Lesson(string[0], string[31] + " " + string[32], string[34] + " " + string[35], venue, lecturer, string[37][:-1])
    subjects[i].lesson.append(lesson)

fn = cwd + "/" + (sys.argv[1][:-5] + ".csv")
with open(fn, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Location'])
    for subject in subjects:
        subjectName = subject.name
        for lesson in subject.lesson:
            date = dayDict[lesson.day]
            for x in range(7):
                writer.writerow([subjectName + " (" + lesson.type + ")", date.strftime("%m/%d/%Y"),
                                 lesson.starttime, date.strftime("%m/%d/%Y"), lesson.endtime, lesson.venue])
                date += datetime.timedelta(days=7)
print(1)
sys.stdout.flush()
