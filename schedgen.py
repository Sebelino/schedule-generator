#!/usr/bin/python2.7

import sys,time,thread,os,argparse,select,csv,datetime
from pprint import pprint
import xml.dom.minidom as minidom

"""
Simple schedule generator.

"""

__author__ = "Sebastian Olsson"

def prettyxml(xml):
    doc = minidom.parseString(xml)
    pretty = doc.toprettyxml(indent="  ",encoding="utf-8")
    return str(pretty)

def intervals(path):
    with open(path,'r') as csvfile:
        reader = csv.reader(csvfile)
        fmt = "%Y-%m-%dT%H:%M:%S"
        timeparse = lambda t: datetime.datetime.fromtimestamp(time.mktime(time.strptime(t,fmt)))
        intervals = [(timeparse(start),timeparse(stop),topic) for (start,stop,topic) in reader]
        return intervals

def myformat(inters):
    year = 2014
    month = 4
    week = inters[0].isocalendar()[1]

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",type=str,metavar='file',default='schedule.csv',
    help="The file which is to be read. If not specified, the output will\
    be written to ./dat/schedule.csv.")
parser.add_argument("-f","--subject",type=str,metavar='subject',
    help="The subject to filter on")
parser.add_argument("-s","--sum",action='store_true',
    help="Sum the results.")
args = parser.parse_args()

working_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = "."
path = os.path.join(data_dir,args.input)

#inters = myformat(intervals(path))
#pprint(inters)

record = {
    'year': 2014, # Year of the first day of the week.
    'week': 4,
    'monday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'tuesday':   [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'wednesday': [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'thursday':  [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'friday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'saturday':  [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'sunday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')]
}

weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
year = record['year']
week = record['week']
html = '<table>'
for day in weekdays:
    dayrecord = record[day]
    dayname = day[0].upper()+day[1:]
    html += '<td><table height="100%">'
    for ((ahrs,amin),(bhrs,bmin),s) in record[day]:
        height = 100*(60*(bhrs-ahrs)+(bmin-amin))/(24*60)
        trtag = '<tr height="%s%%">'% height
        content = s
        trend = '</tr>'
        html += trtag+content+trend
    html += '</table></td>'
html += '</table>'

print prettyxml(html)
#print html

