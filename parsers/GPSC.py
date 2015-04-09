import re, datetime, utils.parser



class Parser:
	regex = re.compile(r'#GPS:(\d+),(\d+),(\d+),f:([A-F0-9]+),f:([A-F0-9]+),f:([A-F0-9]+),(\d+),(\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		
		try:
			time = utils.parser.parseDate(int(m.group(2)),int(m.group(3)))
			startTime = time-datetime.timedelta(seconds=int(m.group(1))/1000.0)
		

			lat = utils.parser.parseFloat(m.group(4))
			lon = utils.parser.parseFloat(m.group(5))
			alt = utils.parser.parseFloat(m.group(6))
			numSats = int(m.group(7))
			hdop = int(m.group(8))

			millis = int(m.group(1))
			return (millis, time, (lat, lon, alt), numSats)
		except Exception as e:
			print e
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#GPS:1329604,80415,18163100,f:E8D91542,f:4B8CF4C2,f:9A196A43,6,132")