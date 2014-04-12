#!/usr/bin/python2.7

import sys,time,thread,os,argparse,select,csv,datetime
import xml.dom.minidom as minidom
from pprint import pprint
from random import randint

"""
Simple schedule generator.

"""

__author__ = "Sebastian Olsson"

WEEKDAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def validaterecord(record):
    pass

def prettyxml(xml):
    doc = minidom.parseString(xml)
    pretty = doc.toprettyxml(indent="  ",encoding="utf-8")
    without_xml_header = pretty.split('\n',1)[1]
    return str(without_xml_header)

def intervals(path):
    with open(path,'r') as csvfile:
        reader = csv.reader(csvfile)
        fmt = "%Y-%m-%dT%H:%M:%S"
        timeparse = lambda t: datetime.datetime.fromtimestamp(time.mktime(time.strptime(t,fmt)))
        intervals = [(timeparse(start),timeparse(stop),topic) for (start,stop,topic) in reader]
        return intervals

def myformat(intervals):
    year = 2014
    month = 4
    week = intervals[0][0].isocalendar()[1]
    record = {'year':year,'week':week}
    for day in WEEKDAYS:
        record[day] = []
    for (start,stop,subject) in intervals:
        day = WEEKDAYS[start.weekday()]
        record[day].append(((start.hour,start.minute),(stop.hour,stop.minute),subject))
    return record

""" If several events with the same subject are too close to each other, they are merged into
one. """
def merge(record):
    for day in WEEKDAYS:
        for i in range(len(record[day])-1):
            (astart,(ahrs,amin),asubject) = record[day][i]
            ((bhrs,bmin),bstop,bsubject) = record[day][i+1]
            if asubject == bsubject and (60*bhrs+bmin)-(60*ahrs+amin) <= 1:
                record[day][i:i+2] = [(astart,bstop,asubject)]
                return merge(record)
    return record

""" Return the content of the file with path 'path', with every occurrence of 'term' replaced by
'replacement'. """
def filecontext(replacement,term,path):
    modcontent = ''
    with open(path,'r') as myfile:
        return ''.join([line.replace(term,replacement) for line in myfile])

def randomcolor():
    return (randint(0,255),randint(0,255),randint(0,255))

""" True if it is okay to pick 'color' as a schedule event color. """
def qualifiedcolor(color,takencolors):
    toodark = sum([c*c for c in color]) < 50**2
    diffs = [tuple([b-a for (a,b) in zip(color,clr)]) for clr in takencolors]
    toosimilar = all([sum([c*c for c in diff]) < 100**2 for diff in diffs])
    return not toodark and not toosimilar

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",type=str,metavar='file',default='data.csv',
    help="The file which is to be read. If not specified, the output will\
    be written to ./data.csv.")
parser.add_argument("-f","--subject",type=str,metavar='subject',
    help="The subject to filter on")
parser.add_argument("-s","--sum",action='store_true',
    help="Sum the results.")
args = parser.parse_args()

data_dir = "."
path = os.path.join(data_dir,args.input)

record = myformat(intervals(path))
record = merge(record)
#pprint(record)
validaterecord(record)

#record = {
#    'year': 2014, # Year of the first day of the week.
#    'week': 4,
#    'monday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
#    'tuesday':   [((7,30),(10,0),'ml'),((10,0),(22,0),'os')],
#    'wednesday': [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
#    'thursday':  [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
#    'friday':    [((5,50),(11,0),'ml'),((13,0),(18,0),'os')],
#    'saturday':  [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
#    'sunday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')]
#}

subjects = set([dayrecord[2] for day in WEEKDAYS for dayrecord in record[day]])
colormap = dict()
for s in subjects:
    color = randomcolor()
    if qualifiedcolor(color,colormap.values()):
        color = randomcolor()
    colormap[s] = color

year = record['year']
week = record['week']

html = '<div class="schedulebox">'

html += '<div class="sidebarbox">'
for h in range(24):
    html += '<div class="sidebartimebox" style="top:%s%%">%02d:00</div>'% (100*h/24.0,h)
html += '</div>'

html += '<div class="weekbox">'
for day in WEEKDAYS:
    dayrecord = record[day]
    dayname = day[0].upper()+day[1:]
    html += '<div class="daybox">'
    html += '<div class="headerbox">%s</div>'% dayname
    for i in range(len(record[day])):
        ((ahrs,amin),(bhrs,bmin),s) = record[day][i]
        height = 100*(60*(bhrs-ahrs)+(bmin-amin))/(24*60.0)
        color = colormap[s]
        top = 100*(60*ahrs+amin)/(24*60.0)
        style = "height:%s%%; top:%s%%; background-color:#%02x%02x%02x"% tuple([height,top]+list(color))
        trtag = '<div class="eventbox" style="%s">'% style
        content = s if height > 2.3 else ' '
        trend = '</div>'
        html += trtag+content+trend
    html += '</div>'
html += '</div>'
html += '</div>'
html = prettyxml(html)

filepath = 'template.html'
term = '{{DATA}}'
context = filecontext(html,term,filepath)
print context
