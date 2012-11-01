# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
import Tkinter as tk
import tkFileDialog
import sys
import numpy
import tkMessageBox
import import_data
import transform_data
import fit_data
import export_data

root = tk.Tk()
root.wm_title("Specview")



# plot the full stopped-flow spectra with a given csv-file
def specfitcsv_plot(file, desc = "", nrview = 6):

    global data

    data = import_data.import_specfit(file)
    (x, data_tr) = transform_data.kin_spec_transform(data)

    myplot.clear()

    # optional labels
    myplot.set_xlabel('wavelength (nm)')
    myplot.set_ylabel('absorbance')
    if desc == "":
        desc = file
    myplot.set_title(desc)
    myplot.set_ylim([-0.02, 2])
    myplot.set_xlim([300, 700])
    #myplot.set_autoscaley_on(False)
    myplot.set_autoscalex_on(False)
    # defining a range of colors to switch between
    colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])

    # plot every single spectrum and change color every time
    sp_counter = 0
    for row in data_tr:
        # print sp_counter % 2
        if sp_counter % nrview == 0:
            color = colors.next()
            myplot.plot(x, row, color, linewidth=0.6)
        sp_counter = sp_counter + 1
    canvas.show()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

def csv3d_plot(file):

    fig = plt.figure()
    my3dplot = fig.gca(projection='3d')

    data = import_data.import_specfit(file)
    (x, data_tr, time) = transform_data.kin_3d_spec(data)

    # optional labels
    my3dplot.set_xlabel('wavelength (nm)')
    my3dplot.set_ylabel('time (s)')
    my3dplot.set_zlabel('absorbance')

    # plot every single spectrum
    sp_counter = 0
    if numpy.amax(data_tr) < 1.5:
        zmax = numpy.amax(data_tr)
    else:
        zmax = 1.5
    for row in data_tr:
        if sp_counter % 6 == 0:
            my3dplot.plot(x, row, zs=time[sp_counter], zdir="y")
            my3dplot.set_zlim3d(-0.02, zmax)
            my3dplot.set_ylim3d(0.0, time[len(time)-1])
        sp_counter = sp_counter + 1
    fig.canvas.set_window_title("Specview 3D Plot")
    plt.show()


# plot a time trace from csv file with a given wavelength
def timetrace_plot(file, wavelength):
    myplot.clear()
    data = import_data.import_specfit(file)
    (time, absorbance, wl_data) = transform_data.timetrace(data, wavelength)

    myplot.set_xlabel("time")
    myplot.set_ylabel("absorbance")
    myplot.set_title(str(wl_data) + " nm")

    myplot.plot(time, absorbance, "b")

    canvas.show()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)


# plot the time trace again, this time with a data fit
# different functions for fitting are possible, also different fitting ranges
def fit_plot(file, wavelength, r_func, xmin, xmax):
    myplot.clear()
    data = import_data.import_specfit(file)
    (time, absorbance, wl_data) = transform_data.timetrace(data, wavelength)

    myplot.set_xlabel("time")
    myplot.set_ylabel("absorbance")
    myplot.set_title(str(wl_data) + " nm")

    myplot.plot(time, absorbance, "b")

    canvas.show()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    (popt, errors) = fit_data.fit_tt(time, absorbance, r_func, xmin, xmax)

    global p_A0
    p_A0.set("A0: " + str(round(popt[0], 4)) + " " + u"\u00B1" + " " + str(round(errors[0], 7)))
    global p_k_ab
    p_k_ab.set("k: " + str(round(popt[2], 4)) + " " + u"\u00B1" + " " + str(round(errors[2], 7)))
    global p_y0
    p_y0.set("y0: " + str(round(popt[1], 4)) + " " + u"\u00B1" + " " + str(round(errors[1], 7)))
    if len(popt) >= 4:
        global p_k_ba
        p_k_ba.set("A1: " + str(round(popt[3], 4)) + " " + u"\u00B1" + " " + str(round(errors[3], 7)))

    #print popt

    if xmax == 0:
        xmax_t = time[-1]
    else:
        xmax_t = xmax
    t = numpy.arange(xmin, xmax_t, 0.05)
    if r_func == "1exp":
        f = popt[0] * numpy.exp(- popt[2] * t) + popt[1]
    if r_func == "2exp":
        f = (popt[0] * numpy.exp(- popt[2] * t)) + popt[1] + (popt[3] * numpy.exp(- popt[4] * t))
    myplot.plot(t, f, "r")

    canvas.show()


#
#
#
# Button-Events:
#
#
#


# button event to plot time trace spectrum
def button_time_tr():
    try:
        global wl
        wl = float(input_wl.get())
        timetrace_plot(file, wl)
    except:
        tkMessageBox.showerror("Error!", "No spectrum loaded.")

# quit the program
def kill():
    if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()
        sys.exit()


# open file and plot
def open_csv():
    global file
    file = tkFileDialog.askopenfilename(title='Choose a file')
    try:
        specfitcsv_plot(file)
    except:
        tkMessageBox.showerror("Error!", "Wrong file format.")


# save data for external use (Origin & co)
def save_csv():
    save_file = tkFileDialog.asksaveasfilename(title="Save as", defaultextension="csv")
    try:
        if "spec_nr" in globals():
            export_data.fullplot_export(data, save_file, spec_nr)
        else:
            export_data.fullplot_export(data, save_file)
    except:
        tkMessageBox.showerror("Error!", "No data exported")

# save transposed data
def save_transposed_data():
    save_file = tkFileDialog.asksaveasfilename(title="Save as", defaultextension="csv")
    try:
        export_data.transpose_export(data, save_file)
    except:
        tkMessageBox.showerror("Error!", "No data exported")




# button event to plot time trace spectrum
def button_time_tr():
    try:
        global wl
        wl = float(input_wl.get())
        timetrace_plot(file, wl)
    except:
        tkMessageBox.showerror("Error!", "Check if spectrum is loaded and a wavelength is selected.")


# button event to do a simple fit and plot it
def button_fit_do():
    try:
        xmin = float(input_xmin.get())
        xmax = float(input_xmax.get())
        r_fitf_input = r_fitf_dd.get()

        global r_func
        if r_fitf_input == "1 Exp + y0":
            r_func = "1exp"
        if r_fitf_input == "2 Exp + y0":
            r_func = "2exp"

        if xmin > xmax:
            tkMessageBox.showerror("Error!", "Error in range definition. Minimum is bigger than maximum")
            return(None)
        if xmin == xmax:
            if xmin != 0:
                tkMessageBox.showerror("Error!", "Error in range definition.")
                return(None)
        fit_plot(file, wl, r_func, xmin, xmax)
    except:
        tkMessageBox.showerror("Error!", "No spectrum loaded or no wavelength selected")


# button event to plot full spectrum (again)
def button_full_spectrum():
    try:
        specfitcsv_plot(file)
    except:
        tkMessageBox.showerror("Error!", "No spectrum loaded.")


def button_3d_spectrum():
    csv3d_plot(file)


#
#
#
# GUI-Elements:
#
#
#

# draw the plot area
def draw_plotarea():
    global fig
    fig = Figure(figsize=(6, 5), dpi=100)
    global myplot
    myplot = fig.add_subplot(111)

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    toolbar = NavigationToolbar2TkAgg( canvas, root )
    toolbar.update()
    canvas._tkcanvas.pack(side='top', fill='both', expand=1)


# draw the pop up window for the time trace
def draw_tt_popup():
    top_tt = tk.Toplevel(root)
    top_tt.geometry("+200+200")
    tk.Label(top_tt, text="Please select a wavelength:").pack()
    global input_wl
    input_wl = tk.Entry(top_tt)
    input_wl.pack(padx=5)
    b = tk.Button(top_tt, text="OK", command=button_time_tr)
    b.pack(pady=5, side=tk.LEFT)
    c = tk.Button(top_tt, text="Close", command=top_tt.destroy)
    c.pack(pady=5, side=tk.RIGHT)


# draw the pop up window to customize the full plot
def draw_customplot_popup():
    top_cp = tk.Toplevel(root)
    top_cp.geometry("+200+200")
    tk.Label(top_cp, text="Title for full spectrum plot:").pack()
    input_title = tk.Entry(top_cp)
    input_title.pack(padx=5)

    nrframe = tk.Frame(top_cp)
    nrframe.pack()

    tk.Label(nrframe, text="Plot every").pack(side=tk.LEFT)
    plotnr = tk.DoubleVar(top_cp)
    plotnr.set(6)
    plotnr_dd = tk.OptionMenu(nrframe, plotnr, 1, 2, 3, 4, 5, 6 , 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
    plotnr_dd.pack(side=tk.LEFT)
    tk.Label(nrframe, text="th spectrum").pack(side=tk.LEFT)

    def customplot_apply():
        title = unicode(input_title.get())
        global spec_nr
        spec_nr = plotnr.get()
        specfitcsv_plot(file, title, spec_nr)

    def customplot_ok():
        title = unicode(input_title.get())
        nr = plotnr.get()
        specfitcsv_plot(file, title, nr)
        top_cp.destroy()


    buttonframe = tk.Frame(top_cp)
    buttonframe.pack(side=tk.BOTTOM)
    
    button_customize1 = tk.Button(buttonframe, text="Apply", command = customplot_apply)
    button_customize1.pack(side=tk.LEFT)
    button_customize2 = tk.Button(buttonframe, text="OK", command = customplot_ok)
    button_customize2.pack(side=tk.LEFT)
    button_customize3 = tk.Button(buttonframe, text="Abort", command = top_cp.destroy)
    button_customize3.pack(side=tk.LEFT)


# draw the pop up window for the simple fitting at one wavelength
def draw_simplefit_popup():
    top_sf = tk.Toplevel(root)
    top_sf.geometry("+200+200")
    tk.Label(top_sf, text="Integrated Rate Law:").pack()
    global r_fitf_dd
    r_fitf_dd = tk.StringVar(top_sf)
    r_fitf_dd.set("1 Exp + y0") # default value 

    fitdd = tk.OptionMenu(top_sf, r_fitf_dd, "1 Exp + y0")
    fitdd.pack()

    tk.Label(top_sf, text="x Range (0 for full spectrum):").pack()

    global input_xmin
    global input_xmax
    input_xmin = tk.Entry(top_sf)
    input_xmax = tk.Entry(top_sf)
    input_xmin.pack()
    input_xmax.pack()
    input_xmin.insert(0, "0")
    input_xmax.insert(0, "0")

    button_fit = tk.Button(top_sf, text="Fit data", command = button_fit_do)
    button_fit.pack(side=tk.LEFT)
    button_close = tk.Button(top_sf, text="Close", command = top_sf.destroy)
    button_close.pack(side=tk.RIGHT)


# Main menu for the program
def draw_menu():
    menu = tk.Menu(root)
    root.config(menu = menu)

    filemenu = tk.Menu(menu)
    menu.add_cascade(label="File", menu = filemenu)
    filemenu.add_command(label="Open...", command = open_csv)
    filemenu.add_separator()
    filemenu.add_command(label="Export multi-spectra csv...", command = save_csv)
    filemenu.add_command(label="Export transposed data...", command = save_transposed_data)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command = kill)

    viewmenu = tk.Menu(menu)
    menu.add_cascade(label="View", menu = viewmenu)
    viewmenu.add_command(label="Full Spectrum", command = button_full_spectrum)
    viewmenu.add_command(label="Customize Plot...", command = draw_customplot_popup)
    viewmenu.add_command(label="Time Trace...", command = draw_tt_popup)
    viewmenu.add_command(label="3D Plot", command = button_3d_spectrum)

    fitmenu = tk.Menu(menu)
    menu.add_cascade(label="Fitting", menu = fitmenu)
    fitmenu.add_command(label="Simple Fitting...", command = draw_simplefit_popup)


# a place for the fitting parameters
def data_area():
    databar = tk.Frame(root)

    l1 = tk.Label(databar, text = "   fitting parameters:   ")
    l1.pack()

    global p_A0
    p_A0 = tk.IntVar()
    p_A0.set("")

    p1 = tk.Label(databar, textvariable = p_A0)
    p1.pack()

    global p_k_ab
    p_k_ab = tk.IntVar()
    p_k_ab.set("")

    p2 = tk.Label(databar, textvariable = p_k_ab)
    p2.pack()

    global p_y0
    p_y0 = tk.IntVar()
    p_y0.set("")

    p3 = tk.Label(databar, textvariable = p_y0)
    p3.pack()

    global p_k_ba
    p_k_ba = tk.IntVar()
    p_k_ba.set("")

    p4 = tk.Label(databar, textvariable = p_k_ba)
    p4.pack()

    databar.pack(side="left", fill="both")


# draw the program window
draw_menu()
data_area()
draw_plotarea()


# catch window manager delete event
root.protocol("WM_DELETE_WINDOW", kill)

root.mainloop()