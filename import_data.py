import sys
import numpy

# get rid of the "data" string
def float_check(value):
	try:
		return(float(value))
	except:
		return(0)

# import special specfit file format
def import_specfit(file):
	return(numpy.loadtxt(open(file, "r"), delimiter=",", skiprows=4, converters = {0: float_check}))