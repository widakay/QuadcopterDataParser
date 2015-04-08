#!/usr/bin/env python

import time, serial, glob, sys, os


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

def findPort():
	serialPorts = listSerialPorts()
	if len(serialPorts) > 0:
		port = serialPorts[0]
		return port
	return

def readInput(port):
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
		return data