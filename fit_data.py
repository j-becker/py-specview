import numpy
import scipy.optimize as opt

# simple fitting at one wavelength. we need the time values(x) and the absorbance values(y).
# third argument is the order of the reaction (default 1).
# a range for fitting can be defined (min, max). it is possible to define starting values for A0 and k. 
def fit_tt(x, y, r_func = "1exp", xmin = 0, xmax = 0, A0 = 0, k = 1):

	# time and absorbance data are transformed into arrays
	x = numpy.array(x)
	y = numpy.array(y)

	sv = []

	# delete elements outside the given fitting range
	if float(xmin) != 0:
		time = 0
		while time < float(xmin):
			x = x[1:]
			y = y[1:]
			time = x[0]

	if float(xmax) != 0:
		time = 99999
		while time > float(xmax):
			x = x[:-2]
			y = y[:-2]
			time = x[-1]


	# definitions of the integrated rate laws
	if r_func == "1exp":
		sv = [-1, 1, 0]
		def func(x, A0, y0, k0):
			return(A0 * numpy.exp(-k0 * x) + y0)
	if r_func == "2exp":
		sv = [1, 0, 1, -1, 0]
		def func(x, A0, y0, k0, A1, k1):
			return((A0 * numpy.exp(-k0 * x)) + (A1 * numpy.exp(-k1 * x)) + y0)


	(popt, pcov) = opt.curve_fit(func, x, y, sv)

	errors = []
	z = 0
	try:
		for row in pcov:
			errors.append(row[z])
			z = z + 1
	except:
		errors = []

	return(popt, errors)
		 