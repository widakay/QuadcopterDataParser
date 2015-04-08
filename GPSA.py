
class GPSA:
	regex = re.compile(r'#GPS:(\d+),(\d+),(\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),([-+]?\d+\.\d+),(\d+),(\d+)')
	def parse(self, string):
		m = self.regex.match(string)
		if not m:
			return
		print m.group(1),m.group(2),m.group(3),m.group(4),m.group(5),m.group(6),m.group(7),m.group(8)
		print line

		try:
			time = parseDate(int(m.group(2)),int(m.group(3)))
			startTime = time-datetime.timedelta(seconds=int(m.group(1))/1000.0)
			print startTime
		except Exception as e:
			print e

		millis = int(m.group(1))
		return (millis)