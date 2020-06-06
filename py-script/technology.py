import random

class Technology:
	def __init__(self, name):
		self.name = name
		self.units = []

	def add_unit(self, unit):
		if unit not in self.units:
			setattr(self, unit, FunctionalUnit(unit))
			self.units += [unit]
			return getattr(self, unit)
		return 0

	def c_define(self, filename, concat = True):
		permissions = 'a' if concat else 'w'
		outfile = open(filename, permissions)

		# for each functional unit
		for u_name in self.units:
			u_str = "#define %s_%s" % (self.name, u_name)
			unit = getattr(self, u_name)
			# for each metric in the functional unit
			for metric in unit.metrics:
				m_str = "%s_%s" % (u_str, metric)
				m_val = getattr(unit, metric)
				m_str = "%-50s %.2e\n" % (m_str, m_val)
				outfile.write(m_str)

			outfile.write("\n")

	def __str__(self):
		out = "%s:" % self.name
		for unit in self.units:
			out += "\n%s" % str(getattr(self, unit))
		return out

class FunctionalUnit:
	def __init__(self, func):
		self.func = func
		self.metrics = []

	def add_metric(self, metric):
		if metric not in self.metrics:
			setattr(self, metric, None)
			self.metrics += [metric]
			return 1
		return 0

	def set_direct(self, metric, value):
		if metric in self.metrics:
			setattr(self, metric, float(value))
			return value
		return 0

	def set_relation(self, metric, conf, ref, rel):
		if metric in self.metrics:
			rand = 1 + random.choice([-1,1])*random.random()*(1-conf)
			value = getattr(ref, metric) * rel * rand
			setattr(self, metric, value)
			return value
		return 0

	def set_calculate(self, metric, conf, ref, calc):
		if metric in self.metrics:
			rand = 1 + random.choice([-1,1])*random.random()*(1-conf)
			value = eval(calc) * rand
			setattr(self, metric, value)
			return value
		return 0

	def __str__(self):
		out = "\t%s:" % self.func
		for metric in self.metrics:
			out += "\n\t\t%s: %.2e" % (metric, getattr(self, metric))
		return out


# test = Technology("tester")
# hi = test.add_unit("add")
# print(hi)
# print(test.add)
# test.add.add_metric("high")
# test.add.set_direct("high", .50)
# print(hi.high)
# print(test)
