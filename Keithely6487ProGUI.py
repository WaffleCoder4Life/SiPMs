import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog, Tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import tkinter.ttk as ttk
from time import sleep, time
import matplotlib.cm as cm
import numpy as np
from itertools import cycle, islice
import threading
from Devices import Keithley6487
#mport pyvisa as visa

class Keithley6487Pro:
    def __init__(self, root):
        self.root = root
        self.root.title("Keithley6487 Pro")
        self.styleb = Style()
        self.styleb.configure(style='my.TButton', font=('Helvetica', 12))
        self.stylel = Style()
        self.stylel.configure(style='my.TLabel', font=('Helvetica', 12))
        self.infostyle = Style()
        self.infostyle.configure(style='info.TLabel', font=('Helvetica', 15))
        self.currstyle = Style()
        self.currstyle.configure(style='curr.TLabel', font=('Helvetica', 35))
        self.running = False
        self.rgb = False
        self.time1 = 0
        self.time2 = None
        self.output = 0
        self.voltData = None
        self.root.protocol('WM_DELETE_WINDOW', self.DESTRUCTION)

        self.plot_window = None

        self.col1 = [cm.rainbow(i) for i in np.linspace(0, 1, 100, endpoint=False)]
        for i in np.linspace(1, 0, 100, endpoint=False):
            self.col1.append(cm.rainbow(i))
        self.colors = cycle(self.col1)
        self.animiter = 0
        
        # Create Keithley6487 object
        self.instr = Keithley6487()

        
        #===========================================FRAMES============================================================================================================

        self.button_frame = Frame(self.root)
        self.button_frame.grid(column=0, row=1)
        self.infoFrame = Frame(self.root)
        self.infoFrame.grid(column=0, row=0)

        #=========================================INFO LABELS=====================================================================================================================

        self.current = '-'
        self.currentLab = Label(self.infoFrame, text=f"{self.current} A", style='curr.TLabel')
        self.currentLab.grid(column=0, row=0, padx=10, pady=20)

        
        self.voltage = float(self.instr.get_voltage())
        self.voltageLab = Label(self.infoFrame, text=f'Voltage: {self.voltage} V', style='info.TLabel')
        self.voltageLab.grid(column=0, row=1, padx=10, pady=10)

      
        self.currentLimit = float(self.instr.get_currLimit())
        self.currentLimitLab = Label(self.infoFrame, text=f'Current limit: {self.currentLimit} A', style='info.TLabel')
        self.currentLimitLab.grid(column=0, row=2, padx=10, pady=10)

        
        self.measurementRange = float(self.instr.get_currRange())
        self.measRanLab = Label(self.infoFrame, text=f'Measurement range: {self.measurementRange} A', style='info.TLabel')
        self.measRanLab.grid(column=0, row=3, padx=20, pady=10)

        #===========================================OPERATING BUTTONS============================================================================================================


        #SAVE
        #self.saveBut = Button(self.button_frame, text="Save", command=self.save, style='my.TButton')
        #self.saveBut.grid(column=3, row=3)

        #CLOSE PROGRAM
        self.stop_button = Button(self.button_frame, text="Close program", command=self.DESTRUCTION, style='my.TButton')
        self.stop_button.grid(column=3, row=10, padx=20, pady=20)


        #SHOW PLOT

        self.plotBut = Button(self.button_frame, text="Open plot", command=self.openPlotScreen, style='my.TButton')
        self.plotBut.grid(column=4, row=1, padx=10)

        #OUTPUT
        self.outputOff = Button(self.button_frame, text="Output Off", command=self.outputOnOff, style='my.TButton')
        self.outputOff.grid(column=3, row=1)
        self.outputOff.grid_remove()

        self.outputOn = Button(self.button_frame, text="Output On", command=self.outputOnOff, style='my.TButton')
        self.outputOn.grid(column=3, row=1)

        #RUN
        #self.runBut = Button(self.button_frame, text="Run", command=self.run, style='my.TButton')
        #self.runBut.grid(column=3, row=1)

        #PAUSE
        #self.pauseBut = Button(self.button_frame, text="Pause", command=self.pause, style='my.TButton')
        #self.pauseBut.grid(column=3, row=2)

        #CLEAR
        #self.clearBut = Button(self.button_frame, text="Clear", command=self.clear, style='my.TButton')
        #self.clearBut.grid(column=3, row=3)

        #RGB
        #self.rgbbut = Button(self.button_frame, text='RGB', command=self.setRgb, style='my.TButton')
        #self.rgbbut.grid(column=4, row=0)
        
        #=========================================VOLTAGE PROGRAM================================================================================================================

        self.setVlabel = Label(self.button_frame, text="Set voltage", style='my.TLabel')
        self.setVlabel.grid(column=0, row=0)
        self.setVentry = Entry(self.button_frame)
        self.setVentry.grid(column=1, row=0)
        self.setVentry.bind('<Return>', self.setVoltage)
        

        self.setILimlabel = Label(self.button_frame, text="Set current limit", style='my.TLabel')
        self.setILimlabel.grid(column=0, row=1)
        self.setILimentry = Entry(self.button_frame)
        self.setILimentry.grid(column=1, row=1)
        self.setILimentry.bind('<Return>', self.setCurrentLimit)
        

        self.setMeasRanlabel = Label(self.button_frame, text="Measurement range", style='my.TLabel')
        self.setMeasRanlabel.grid(column=0, row=2)
        self.setMeasRanentry = Entry(self.button_frame)
        self.setMeasRanentry.grid(column=1, row=2)
        self.setMeasRanentry.bind('<Return>', self.setMeasurementRange)

        
        
        
    
    #=======================================================FUNCTIONS==================================================================================================
    
    def setRgb(self):
        if self.rgb is False:
            self.rgb = True
        else:
            self.rgb = False

    def openPlotScreen(self):
        self.plot_window = PlotWindow(self)

    
    def outputOnOff(self):
        if self.output == 0:
            self.instr.command(":FORM:ELEM READ") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
            self.instr.command(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
            self.instr.command(":SOUR:VOLT:STAT ON")
            self.output = 1
            self.running = True
            self.updateCurrent()
            self.outputOn.grid_remove()
            self.outputOff.grid(column=3, row=1)

        elif self.output == 1:
            self.running = False
            self.instr.command(":SOUR:VOLT:STAT OFF")
            self.output = 0
            self.outputOff.grid_remove()
            self.outputOn.grid(column=3, row=1)


    

    def setVoltage(self, event=None):
        self.voltage = self.setVentry.get()
        self.instr.command(f":SOUR:VOLT {self.voltage}")
        self.instr.command(":SOUR:VOLT?")
        self.voltage = float(self.instr.read())
        self.voltageLab.config(text=f'Voltage: {self.voltage} V')
        self.setVentry.delete(0, 'end')
        #sleep(2)
    
    def setCurrentLimit(self, event=None):
        self.currentLimit = float(self.setILimentry.get())
        self.instr.set_currLimit(self.currentLimit)
        self.currentLimit = self.instr.get_currLimit()
        self.currentLimitLab.config(text=f"Current limit: {self.currentLimit:.2e} A")
        self.setILimentry.delete(0, 'end')

    
    def setMeasurementRange(self, event=None):
        self.measurementRange = self.setMeasRanentry.get()
        self.setMeasRanentry.delete(0, 'end')
        if float(self.measurementRange) < -0.021:
            self.instr.command(f":CURR:RANG -0.021")
            self.instr.command(":CURR:RANG?")
            self.measurementRange = float(self.instr.read())
            self.measRanLab.config(text=f'Measurement range: {self.measurementRange} A')
        elif float(self.measurementRange) > 0.021:
            self.instr.command(f":CURR:RANG 0.021")
            self.instr.command(":CURR:RANG?")
            self.measurementRange = float(self.instr.read())
            self.measRanLab.config(text=f'Measurement range: {self.measurementRange} A')
        else:
            self.instr.command(f":CURR:RANG {self.measurementRange}")
            self.instr.command(":CURR:RANG?")
            self.measurementRange = float(self.instr.read())
            self.measRanLab.config(text=f'Measurement range: {self.measurementRange} A')


    def pause(self):
        self.time2 = time()
        self.instr.command(":SOUR:VOLT:STAT OFF")
        self.running = False
        

    def run(self):
        self.instr.command(":FORM:ELEM READ") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
        self.instr.command(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
        self.instr.command(":SOUR:VOLT:STAT ON")
        #self.instr.command(f":SOUR:VOLT:ILIM {self.currentLimit}") # Set the maximum current limit
        #self.instr.command(f":SENS:RANG {self.measurementRange}")
        if self.time2 is None:
            self.time1 = time()
        else:
            self.time1 = self.time2

        self.running = True
        self.updateCurrent()

    def updateCurrent(self):
        if self.running:
            self.instr.command(":INIT") #TRIGGER MEASUREMENT
            self.instr.command(":SENS:DATA?") # data plz UwU
            self.voltData = float(self.instr.read())
            self.currentLab.config(text=f'{self.voltData:.3e} A')
            self.root.after(1000, self.updateCurrent)  # update plot every 100 ms

    

    def save(self):
        self.running = False
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filename:
            self.fig.savefig(filename)
    
    def DESTRUCTION(self):
        self.instr.closeResource()
        self.root.quit()

    def clear(self):
        self.xdata = []
        self.ydata = []
        self.ax.clear()
        self.ax.set_ylabel("Current / A")
        self.ax.set_xticks([])
        self.canvas.draw()
        self.currentLab.config(text='- A')

class PlotWindow:
    def __init__(self, parent):
        self.parent = parent
        self.new_window = tk.Toplevel(self.parent.root)
        self.new_window.title("IV plot")

        self.parent.instr.command(":FORM:ELEM READ") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
        self.parent.instr.command(":FORM:DATA ASCii") #CHOOSE DATA FORMAT


        self.fig, self.ax = plt.subplots()
        self.fig.set_figheight(12 / 16 * 9)
        self.fig.set_figwidth(12)
        self.sc = self.ax.scatter([], [])
        self.ax.set_ylabel("Current / A")
        self.ax.set_xticks([])
        
        self.xdata, self.ydata = [], []
        

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.new_window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=1, row=0)

        self.update_plot()

    def update_plot(self):

        if self.parent.voltData == None:
            print("Turn output on!!")
        
        else:

            self.xdata.append(len(self.xdata))
            self.ydata.append(self.parent.voltData)
        
            #self.ax.collections.clear()
            self.sc = self.ax.scatter(self.xdata, self.ydata, color='black')
            self.canvas.draw()
            #self.currentLab.config(text=f'{ydat:.3e} A')
            self.new_window.after(1000, self.update_plot)  # update plot every 100 ms

            return self.sc,


if __name__ == '__main__':
    root = Tk()
    app = Keithley6487Pro(root)
    root.mainloop()