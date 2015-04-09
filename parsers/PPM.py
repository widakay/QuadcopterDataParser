import re, datetime, utils



class Parser:
	regex = re.compile(r'#PPM:(\d+),(\d+\.\d+),([-+]?\d+\.\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		millis = int(m.group(1))
		voltage = float(m.group(2)) * 3.3 / 1024
		ppm = float(m.group(3))
		return (millis, voltage, ppm)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#PPM:22427,426.40,0.1365")