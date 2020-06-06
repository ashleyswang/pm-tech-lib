import yaml
from technology import Technology, FunctionalUnit

def import_yaml(infile):
	lib = yaml.safe_load(open(infile, 'r'))
	
	tech = Technology(lib['tech'])

	# Add functional unit to technology
	for u_name in lib['func_unit']:
		unit = tech.add_unit(u_name)

		# Add metric to functinal unit
		for m_name in lib['func_unit'][u_name]:
			assert (unit.add_metric(m_name)), "add metric failed"
			metric = lib['func_unit'][u_name][m_name]
			# Know value of metric 
			if type(metric) is float:
				unit.set_direct(m_name, metric)
			# Need to calculate or use relation
			else:
				ref = eval(metric['ref']) if ('ref' in metric) else None
				rel = metric['rel'] if ('rel' in metric) else None
				calc = metric['calc'] if ('calc' in metric) else None
				conf = metric['conf']

				if rel is not None:
					unit.set_relation(m_name, conf, ref, rel)
				elif calc is not None:
					unit.set_calculate(m_name, conf, ref, calc)
	return tech


# Test functions

cmos40_aladdin = import_yaml('../func-unit-est/cmos40_aladdin-lib.yaml')
print(cmos40_aladdin)
# print(cmos40_aladdin.reg)

cnfet = import_yaml('../func-unit-est/cnfet-lib.yaml')
print(cnfet)

cmos40_aladdin.c_define('test.c', concat = False)
cnfet.c_define('test.c')