# TARUC TimeTable to CSV
Generate Google Calendar CSV from TARUC Intranet  

### Dependencies
* [Python 3](https://www.python.org/downloads/) 

* BeautifulSoup 4  
```
pip install beautifulsoup4
```

### Usage
Use "Save as..." in your browser to download timetable from TARUC Intranet,  

Then excecute
```
python timetable.py [timetable html]
```

### Precaution
This script is currently assuming short sem (7 weeks).
If there's any replacement class on the table it will most probably break the script.
