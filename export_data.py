import sys
import csv
import numpy

# gets numpy array with raw data from import, filename to save csv and information which xth spectrum to use

def fullplot_export(data_imp, save_file, spec_nr = 6):
	writer = csv.writer(open(save_file,"w"), delimiter=",")
	# write the time row
	data_imp = numpy.transpose(data_imp)
	temp_data = []
	temp_data.append(data_imp[0,:])
	# set counter to 1 to get rid of the time row
	c = 1
	for row in list(data_imp):
		if c % spec_nr == 0:
			temp_data.append(row)
		c = c + 1
	data_imp = numpy.transpose(temp_data)

	for row in list(data_imp):
		writer.writerow(row)


# gets numpy array with raw data from import, filename to save csv 
# and saves the transposed data matrix for kinetic evaluation

def transpose_export(data_imp, save_file):
	writer = csv.writer(open(save_file,"w"), delimiter=",")
	for row in list(numpy.transpose(data_imp)):
		writer.writerow(row)
