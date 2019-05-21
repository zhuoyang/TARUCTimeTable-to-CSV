import sys
import urllib.request
import pathlib
import datetime
import csv
import os
import ptvsd
from bs4 import BeautifulSoup

#VS Code debugger
# print("Waiting for debugger attach")
# sys.stdout.flush()
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()

if len(sys.argv) == 3:
    if sys.argv[2] == "node":
        cwd = os.path.dirname(os.path.abspath(__file__))
        page = urllib.request.urlopen("file:///" + cwd + "/" + sys.argv[1])
else:
    page = urllib.request.urlopen("file:///" + sys.argv[1])

soup = BeautifulSoup(page, 'html5lib')
allTable = soup.findAll('table', {'id': 'simple-table'})
table = allTable[1].find('tbody').findAll('tr')

# find how many study weeks in this sem
semDate = soup.find('div', {'class': 'form-group'}).findAll('label')[1].contents[2].split(" ")
semStartDate = semDate[4]
semEndDate = semDate[7]
semStartDateTime = datetime.datetime.strptime(semStartDate, "%Y-%m-%d")
semEndDateTime = datetime.datetime.strptime(semEndDate, "%Y-%m-%d")
semDuration = int(((semEndDateTime - semStartDateTime).days + 1) / 7) 
dayDict = {
    "Mon": semStartDateTime,
    "Tue": semStartDateTime + datetime.timedelta(days=1),
    "Wed": semStartDateTime + datetime.timedelta(days=2),
    "Thu": semStartDateTime + datetime.timedelta(days=3),
    "Fri": semStartDateTime + datetime.timedelta(days=4),
    "Sat": semStartDateTime + datetime.timedelta(days=5),
    "Sun": semStartDateTime + datetime.timedelta(days=6)
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
    lesson = Lesson(string[0], string[31] + " " + string[32], string[34] + " " + string[35], venue, lecturer, string[37][:-1])
    subjects[i].lesson.append(lesson)
if len(sys.argv) == 3:
    if sys.argv[2] == "node":
        fn = cwd + "/" + (sys.argv[1][:-5] + ".csv")
else:
    fn = "timetable.csv"
with open(fn, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Location', 'Description'])
    for subject in subjects:
        subjectName = subject.name
        for lesson in subject.lesson:
            date = dayDict[lesson.day]
            for x in range(semDuration):
                writer.writerow([subjectName + " (" + lesson.type + ")", date.strftime("%m/%d/%Y"),
                                 lesson.starttime, date.strftime("%m/%d/%Y"), lesson.endtime, lesson.venue, lesson.lecturer])
                date += datetime.timedelta(days=7)
print(1)
sys.stdout.flush()
