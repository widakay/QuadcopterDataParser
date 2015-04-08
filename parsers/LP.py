import re, datetime, utils



class LP:
	regex = re.compile(r'#LP:(\d+),(\d+),(\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return

		millis = int(m.group(1))
		return (millis)
if __name__ == "__main__":
	parser = LP()
	print parser.parse("hi")
	print parser.parse("#LP:2229229,1,191")