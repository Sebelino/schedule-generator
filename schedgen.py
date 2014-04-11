#!/usr/bin/python2.7

import sys,time,thread,os,argparse,select,csv,datetime

"""
Simple schedule generator.

"""

__author__ = "Sebastian Olsson"

def deltas(path):
    with open(path,'r') as csvfile:
        reader = csv.reader(csvfile)
        fmt = "%Y-%m-%dT%H:%M:%S"
        timeparse = lambda t: datetime.datetime.fromtimestamp(time.mktime(time.strptime(t,fmt)))
        intervals = [(timeparse(stop)-timeparse(start),topic) for (start,stop,topic) in reader]
        return intervals

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

intervals = deltas(path)
if args.subject:
    intervals = [(t,s) for (t,s) in intervals if s == args.subject]
datesum = datetime.timedelta(0)
for (t,s) in intervals:
    datesum += t
output = [[datesum]] if args.sum else intervals
for row in output:
    print ' '.join([str(cell) for cell in row])
