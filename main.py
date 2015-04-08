#!/usr/bin/env python

import time
import os
import sys
import datetime
import struct
import parsers
import serInput
import inspect

directory = "data/" + "sample-desk" #str(int(time.time()))

if len(sys.argv) > 1:
	directory = sys.argv[1]

if not os.path.exists(directory):
	os.makedirs(directory)

filename = directory + "/data.txt"


print "openning", filename

port = serInput.findPort()
if port:
	dataFile = open(filename, "w")

	dataFile.write(serInput.readInput(port))

	dataFile.close()
else:
	print "using cached data"

import types
parserList = {}
for name, module in parsers.__dict__.iteritems():
	if type(module) is types.ModuleType:
		for name2, parser in module.__dict__.iteritems():
			if type(parser) is types.ClassType:
				if name == name2:
					print "adding parser:", name2
					parserList[name] = parser()
#print parserList


log = open(filename, "r")
fileshort = filename[:filename.find(".txt")]
print fileshort

gps = open(fileshort+"-GPS.kml", "w")
pos = open(fileshort+"-POS.csv", "w")
imu = open(fileshort+"-dat.csv", "w")

gps.write("Stuff\n")
imu.write("Time,prs,ax,ay,az,gx,gy,gz,mx,my,mz\n")
pos.write("Time,x,y,z\n")


posVec = [0,0,0]

startTime = datetime.datetime.now()
lasttime = 0
for line in log.readlines():
	line = line.strip()
	for mType, parser in parserList.iteritems():
		m = parser.parse(line)
		if m:
			print mType + ":", m
	#print line
