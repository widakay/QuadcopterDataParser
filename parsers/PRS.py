import re, datetime, utils.parser



class Parser:
	regex = re.compile(r'#PRS:(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		
		millis = int(m.group(1))
		temperature = float(m.group(2))
		pressure = float(m.group(3))
		return (millis, pressure, temperature)
if __name__ == "__main__":
	parser = Parser()
	print parser.parse("hi")
	print parser.parse("#PRS:182794,23.10,992.5100")