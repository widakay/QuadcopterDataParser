#!/usr/bin/env python

import time
import os
import sys
import datetime
import struct
import parsers
import serInput
import inspect
import simplekml
import types

directory = "data/" + "park-good1"#withwalk"# + str(int(time.time()))

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

parserList = {}
for name, module in parsers.__dict__.iteritems():
	if type(module) is types.ModuleType:
		for name2, parser in module.__dict__.iteritems():
			if type(parser) is types.ClassType:
				if name2 == "Parser":
					print "adding parser:", name
					parserList[name] = parser()

# 	GPS example:
#		#GPS:2136,12,37.462688,-122.274070,229.20,9,114
#		$GPS:1651585,f:E6D91542,f:488CF4C2,f:00000041,f:00000043:#
#		#GPS:2505,80415,17542400,f:EDD91542,f:538CF4C2,f:CD4C6643,6,126
#	IMU example:
#		#IMU:343808,25.31,-7,-7,-7,-55,118,29,956,0,16736:#

parsers.testParsers(parserList)


log = open(filename, "r")
fileshort = filename[:filename.find(".txt")]
print fileshort


pos = open(fileshort+"-GPS.csv", "w")
pos.write("Time,Lat,Lon,Alt\n")

lp = open(fileshort+"-LP.csv", "w")
lp.write("Time,heater,voltage\n")

ppm = open(fileshort+"-PPM.csv", "w")
ppm.write("Time,voltage,ppm\n")

prs = open(fileshort+"-PRS.csv", "w")
prs.write("Time,pressure,temperature\n")

imu = open(fileshort+"-IMU.csv", "w")
imu.write("Time,prs,ax,ay,az,gx,gy,gz,mx,my,mz\n")



posVec = [0,0,0]
data = []

lastPressure = 0
lastTemp = 0
lastPPM = 0
lastLP = 0


startTime = datetime.datetime.now()
lasttime = 0

for line in log.readlines():
	line = line.strip()
	for mType, parser in parserList.iteritems():
		m = parser.parse(line)
		if m:
			print mType.ljust(6) + ":", m
			if mType == "PRS":
				lastPressure = m[1]
				lastTemp = m[2]
				prs.write(str(m[0]) + "," + str(m[1]) + "," + str(m[2]) + '\n')
			elif mType == "PPM":
				lastPPM = m[2]
				ppm.write(str(m[0]) + "," + str(m[1]) + "," + str(m[2]) + '\n')
			elif mType == "LP":
				lastLP = m[2]
				lp.write(str(m[0]) + "," + str(m[1]) + "," + str(m[2]) + '\n')
			elif mType == "GPSC":
				if m[2][2] < 100000:
					data.append((m[1], (m[2][1], m[2][0], m[2][2]), lastPressure, lastLP, lastPPM, lastTemp))
				pos.write(str(m[1]) + "," + str(m[2][0]) + "," + str(m[2][1]) + "," + str(m[2][2]) + '\n')


from operator import itemgetter

print data[0]

def createKML(sensorID):
	kml = simplekml.Kml()
	chartval = sensorID
	minimum = min(data,key=lambda item:item[chartval])[chartval]
	maximum = max(data,key=lambda item:item[chartval])[chartval]

	print sensorID, maximum, minimum, (data[0][chartval]-minimum)*(255.0/(maximum-minimum))

	for i in xrange(len(data)-2):
		linestring = kml.newlinestring()
		linestring.coords = [data[i][1],data[i+1][1]]
		color = (data[i][chartval]-minimum)*(255.0/(maximum-minimum))
		r = color
		g = 255-color
		b = 255
		linestring.style.linestyle.color = "aa%02x%02x%02x" % (b,g,r)
		linestring.altitudemode = simplekml.AltitudeMode.absolute
		linestring.style.linestyle.width = 10

	kml.save(fileshort+"-"+str(sensorID)+".kml")



for i in range(2,6):
	createKML(i)