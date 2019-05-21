# TARUC TimeTable to CSV
Generate Google Calendar CSV from TARUC Intranet  

### Dependencies
* [Python 3.7.x](https://www.python.org/downloads/) 

* BeautifulSoup 4  
```
pip install beautifulsoup4
```
* html5lib  
```
pip install html5lib
```

### Usage
1) Use "Save as..." in your browser to download timetable from TARUC Intranet.  

2) Execute
```
python timetable.py [full path to timetable html]
```
3) File named "timetable.csv" will be generated in the same folder.

### Web Server Usage
- [Node.js](https://nodejs.org/en/) is needed for web server  

- To install dependencies, execute:
```
npm install
```
- To run the web server, execute: 
```
node webserver.js
```

### Precaution
- Alternating class would most probably not working, please create an issue with your timetable so that I can fix it.
- Replacement class is excluded
