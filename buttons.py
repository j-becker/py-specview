#import matplotlib
#matplotlib.use('TkAgg')
 
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
import itertools
import Tkinter as tk
import tkFileDialog
import sys
import numpy
import tkMessageBox
import import_data
import transform_data
import fit_data

# button event to plot time trace spectrum
def button_time_tr():
    try:
        global wl
        wl = float(input_wl.get())
        timetrace_plot(file, wl)
    except:
        tkMessageBox.showerror("Error!", "No spectrum loaded.")