#!/usr/bin/env python

import time
import serial
import glob
import re
import os
import sys
import datetime
import struct

directory = "data/" + "sample-desk" #str(int(time.time()))

if len(sys.argv) > 1:
	directory = sys.argv[1]

if not os.path.exists(directory):
	os.makedirs(directory)

filename = directory + "/data.txt"


print "openning", filename


def listSerialPorts():
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class UnknownSerialPortException(Exception):
    pass

serialPorts = listSerialPorts()
if len(serialPorts) > 0:
	port = serialPorts[0]

if not os.path.exists(port):
	raise UnknownSerialPortException("Port " + port + " does not exist")
else:
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
		port=port,
		baudrate=115200,
		parity=serial.PARITY_ODD,
		stopbits=serial.STOPBITS_TWO,
		bytesize=serial.SEVENBITS
	)


	if ser.isOpen():
		print "Port already open..."
	else:
		print "Openning port..."
		ser.open()


	ser.flush()


	ser.write("rd")

	end = time.time() + 2
	print "reading data...."
	
	data = ""
	while time.time() < end:
		while ser.inWaiting():
			addition = ser.read(ser.inWaiting())
			data += addition
			print 'Receieved \t' + str(len(addition)) + " bytes"
			end = time.time() + 0.75
		time.sleep(0.5)
	#print data

	ser.close()

	dataFile = open(filename, "w")

	dataFile.write(data)

	dataFile.close()

	

# 	GPS example:
#		#GPS:2136,12,37.462688,-122.274070,229.20,9,114
#		$GPS:1651585,f:E6D91542,f:488CF4C2,f:00000041,f:00000043:#
#		#GPS:2505,80415,17542400,f:EDD91542,f:538CF4C2,f:CD4C6643,6,126
#	IMU example:
#		#IMU:343808,25.31,-7,-7,-7,-55,118,29,956,0,16736:#

messages = {

	# #GPS:4024,14,37.462688,-122.274070,229.50,9,114
	'GPSA': re.compile(r'#GPS:(\d+),(\d+),(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),(\d+),(\d+)'), #,(\d+),(\d+),(\d+),(\d+)'),

	# $GPS:1651585,f:E6D91542,f:488CF4C2,f:00000041,f:00000043:#
	'GPSB': re.compile(r'\$GPS:(\d+),f:([A-F0-9]+),f:([A-F0-9]+),f:([A-F0-9]+),f:([A-F0-9]+)'),

	# #GPS:2505,80415,17542400,f:EDD91542,f:538CF4C2,f:CD4C6643,6,126
	'GPSC': re.compile(r'#GPS:(\d+),(\d+),(\d+),f:([A-F0-9]+),f:([A-F0-9]+),f:([A-F0-9]+),(\d+),(\d+)'),

	# 
	'PRS': re.compile(r'#PRS:(\d+),(\d+),(\d+)'),

	#
	'IMU': re.compile(r'#IMU:(\d+),([-+]?\d+\.\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+),([-+]?\d+)'),

	# #PPM:3729,411,0.0768
	'PPM': re.compile(r'#PPM:(\d+),(\d+),([-+]?\d+\.\d+)'),

	# #BATT:5019,69.30,3.8489
	'BAT': re.compile(r'#BAT:(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+)'),

	# #LP:5711,0,12
	'LP': re.compile(r'#LP:(\d+),(\d+),(\d+)'),
}


def decodeFloat(inString):
	return struct.unpack('f', inString.decode("hex"))[0]


def parseDate(date,time):
	if date<10000:
		raise Exception("Invalid Date")
	year=date%100
	print date, time, year
	if year != 15:
		year = 15
	if year>80:
		year += 1900
	else:
		year += 2000
	month = (date/100)%100
	day = date/10000
	hour = time / 1000000
	minute = (time / 10000) % 100
	second = (time / 100) % 100

	print year,month,day,hour,minute,second
	return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

class message():
	def __init__(self):
		self.re = None
	def match(self, string):
		return self.re.match(string)

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
	
	for mType, message in messages.iteritems():
		m = message.match(line)
		if m:
			print mType + ":", m.group(0)

		if m and mType == "GPSA":
			#print m.group(1),m.group(2),m.group(3),m.group(4),m.group(5),m.group(6),m.group(7),m.group(8)
			#print line

			try:
				time = parseDate(int(m.group(2)),int(m.group(3)))
				startTime = time-datetime.timedelta(seconds=int(m.group(1))/1000.0)
				print startTime
			except Exception as e:
				print e

			millis = int(m.group(1))

		if m and mType == "GPSB":
			arduinoTime = int(m.group(1))

			#print line
			#print decodeFloat(m.group(2)), decodeFloat(m.group(3)), decodeFloat(m.group(4)), decodeFloat(m.group(5))
			try:
				time = parseDate(int(m.group(2)),int(m.group(3)))
				startTime = time-datetime.timedelta(seconds=int(m.group(1))/1000.0)
				print startTime
			except Exception as e:
				print e

			millis = int(m.group(1))

		elif m and mType == "PRS":
			#print "2"
			if int(m.group(1))/1000.0 < lasttime:
				print "Time went backwards... skipping data"
				startTime = "invalid"
			else:
				#print m.group()
				if startTime != "invalid":
					imu.write(str((startTime+datetime.timedelta(seconds=int(m.group(1))/1000.0)))+","+m.group(2)+","+m.group(3)+"\n")
					lasttime = int(m.group(1))/1000.0
		elif m and mType == "IMU":
			#print "3"
			#print m.group(0)
			#print m.group(1), m.group(2), m.group(3), m.group(4)
			
			time = int(m.group(1))/1000.0
			accel = [float(m.group(8))/512, float(m.group(9))/512, float(m.group(10))/512]
			if lasttime != 0:
				timedelta = time-lasttime
			else:
				timedelta = 0	# ignore first reading

			posVec[0] += accel[0] * timedelta
			posVec[1] += accel[1] * timedelta
			posVec[2] += accel[2] * timedelta

			print timedelta, accel, posVec

			pos.write(str(time)+","+str(posVec[0])+","+str(posVec[1])+","+str(posVec[2])+"\n")

			if startTime != "invalid":
				imu.write(str((startTime+datetime.timedelta(seconds=int(m.group(1))/1000.0)))+","+m.group(2)+","+m.group(3)+"\n")
				lasttime = time
		elif m and mType == "PPM":
			pass
		elif m and mType == "BAT":
			pass
		elif m and mType == "LP":
			pass
		elif m:
			pass
		else:
			pass
		






