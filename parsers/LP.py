import re, datetime, utils



class Parser:
	regex = re.compile(r'#LP:(\d+),(\d+),(\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return

		millis = int(m.group(1))
		heater = int(m.group(2))
		val = int(m.group(3))

		return (millis, heater, val)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#LP:2229229,1,191")