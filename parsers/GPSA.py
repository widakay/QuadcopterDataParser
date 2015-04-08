import re, datetime, utils



class GPSA:
	regex = re.compile(r'#GPS:(\d+),(\d+),(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),(\d+),(\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return

		try:
			time = parseDate(int(m.group(2)),int(m.group(3)))
			startTime = time-datetime.timedelta(seconds=int(m.group(1))/1000.0)
			
		except Exception as e:
			print e

		millis = int(m.group(1))
		return (millis)
if __name__ == "__main__":
	parser = GPSA()
	print parser.parse("hi")
	print parser.parse("#GPS:1329604,80415,18163100,f:E8D91542,f:4B8CF4C2,f:9A196A43,6,132")