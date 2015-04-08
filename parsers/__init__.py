
import re, datetime

import os


for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module

# 	GPS example:
#		#GPS:2136,12,37.462688,-122.274070,229.20,9,114
#		$GPS:1651585,f:E6D91542,f:488CF4C2,f:00000041,f:00000043:#
#		#GPS:2505,80415,17542400,f:EDD91542,f:538CF4C2,f:CD4C6643,6,126
#	IMU example:
#		#IMU:343808,25.31,-7,-7,-7,-55,118,29,956,0,16736:#
"""
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

			"""



if __name__ == "__main__":
	import inspect, sys
	parserList = {}
	for name, classref in inspect.getmembers(sys.modules[__name__]):
		print name
	sys.exit(0)
	for name, parser in inspect.getmembers(sys.modules[__name__], inspect.isclass):
		parserList[name] = parser()

	for parser in parserList.values():
		print "Bad Data:\t", parser.parse("hi")
		print "GPSC:\t\t", parser.parse("#GPS:1329604,80415,18163100,f:E8D91542,f:4B8CF4C2,f:9A196A43,6,132")
	