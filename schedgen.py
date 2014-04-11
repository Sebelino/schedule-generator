#!/usr/bin/python2.7

import sys,time,thread,os,argparse,select,csv,datetime
import xml.dom.minidom as minidom
from pprint import pprint
from random import randint

"""
Simple schedule generator.

"""

__author__ = "Sebastian Olsson"

def prettyxml(xml):
    doc = minidom.parseString(xml)
    pretty = doc.toprettyxml(indent="  ",encoding="utf-8")
    without_xml_header = pretty.split('\n',1)[1]
    return str(without_xml_header)

def sidebarhtml():
    with open('sidebar.html','r') as myfile:
        return ''.join(myfile.readlines())

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

working_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = "."
path = os.path.join(data_dir,args.input)

#inters = myformat(intervals(path))
#pprint(inters)

record = {
    'year': 2014, # Year of the first day of the week.
    'week': 4,
    'monday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'tuesday':   [((7,30),(10,0),'ml'),((10,0),(22,0),'os')],
    'wednesday': [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'thursday':  [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'friday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'saturday':  [((4,30),(10,0),'ml'),((10,0),(15,0),'os')],
    'sunday':    [((4,30),(10,0),'ml'),((10,0),(15,0),'os')]
}

weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

subjects = set([dayrecord[2] for day in weekdays for dayrecord in record[day]])
colormap = dict()
for s in subjects:
    color = randomcolor()
    if qualifiedcolor(color,colormap.values()):
        color = randomcolor()
    colormap[s] = color

year = record['year']
week = record['week']

html = '<table class="weektable">'
html += '<td>%s</td>'% sidebarhtml()
for day in weekdays:
    dayrecord = record[day]
    dayname = day[0].upper()+day[1:]
    html += '<td><table class="daytable">'
    initheight = 100*(60*record[day][0][0][0]+record[day][0][0][1])/(24*60.0)
    html += '<tr><td height="%s%%"></td></tr>'% initheight
    for i in range(len(record[day])):
        ((ahrs,amin),(bhrs,bmin),s) = record[day][i]
        height = 100*(60*(bhrs-ahrs)+(bmin-amin))/(24*60.0)
        color = colormap[s]
        trtag = '<tr><td class="eventtd" height="%s%%" bgcolor="#%02x%02x%02x">'% tuple([height]+list(color))
        content = s
        trend = '</td></tr>'
        html += trtag+content+trend
        trailingheight = 100*(60*((record[day][i+1][0][0] if i+1 < len(record[day]) else 24)-bhrs)+((record[day][i+1][0][1] if i+1 < len(record[day]) else 0)-bmin))/(24*60.0)
        html += '<tr><td height="%s%%"></td></tr>'% initheight
    html += '</table></td>'
html += '</table>'
html = prettyxml(html)

filepath = 'template.html'
term = '{{DATA}}'
context = filecontext(html,term,filepath)
print context
