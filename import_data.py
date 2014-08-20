import sys
import numpy
import os

# get rid of the "data" string
def float_check(value):
	try:
		return(float(value))
	except:
		return(0)


# import special specfit file format
def import_specfit(file):
	return(numpy.loadtxt(open(file, "r"), delimiter=",", skiprows=4, converters = {0: float_check}))


# import special specfit file format (the old ones)
def import_oldspecfit(file):
	f = open(file, "r")
	tempfile = open("tempfile", "w")
	for line in f:
		line = line.replace(",",".")
		tempfile.write(line)
	tempfile.close()
	f.close()
	data = numpy.loadtxt(open("tempfile", "r"), delimiter=";", skiprows=7, converters = {0: float_check})
	os.remove("tempfile")
	return(data)
