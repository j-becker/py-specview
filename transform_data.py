import numpy

def kin_spec_transform(data_imp):
	# extract first column as list of x, other columns are transposed and transformed into a list
	# returns a list for x and a list of arrays for the absorption data
	data_imp = numpy.delete(data_imp, 0, 0)
	x = list(data_imp[:,0])
	data_imp = numpy.delete(data_imp, 0, 1)
	return(x, list(numpy.transpose(data_imp)))

def kin_3d_spec(data_imp):
	temp_data = numpy.delete(data_imp, 0, 0)
	wl = list(temp_data[:,0])

	temp_data = numpy.transpose(data_imp)
	if temp_data[0,0] == 0:
		time = list(numpy.delete(temp_data[:,0], 0, 0))
	else:
		time = list(temp_data[:,0])

	data_imp = numpy.delete(data_imp, 0, 0)
	data_imp = numpy.delete(data_imp, 0, 1)

	return(wl, list(numpy.transpose(data_imp)), time)


# we take the input data and a wavelength and return time and absorbance values
def timetrace(data_imp, wavelength):
	wl_column = 0
	nr = 0
	data_imp = numpy.transpose(data_imp)
	# fix for the "data" string problem to get lists of equal length
	if data_imp[0,0] == 0:
		time = list(numpy.delete(data_imp[:,0], 0, 0))
	else:
		time = list(data_imp[:,0])

	# check every column until the selected wavelength is reached
	while wl_column < float(wavelength):
		nr = nr + 1
		wl_column = data_imp[0,nr]
	return(time, list(numpy.delete(data_imp[:,nr], 0, 0)), wl_column)
