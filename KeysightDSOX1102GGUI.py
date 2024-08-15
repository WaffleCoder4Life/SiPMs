from Devices import DSOX1102G
from tkinter.ttk import *
import tkinter as tk
import dataHandling as data
import threading
import dataHandling as data


class DSOX1102GGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DSOX1102G")

        self.root.protocol('WM_DELETE_WINDOW', self.DESTRUCTION) # pressing 'x' closes


        # Create DSOX1102G object and reset
        self.instr = DSOX1102G()
        #self.instr.resetFactory() # Uncomment to reset

        # Set screen
        self.instr.setDisplay(1, 160e-3, 1)
        self.instr.setDisplay(2, 8, 500e-9)
        self.instr.setTriggerValue(0)
        self.timeRang = 1e-6
        self.instr.command(":STOP")

        
        #======================FRAMES==========================================
        self.runFrame = Frame(self.root)
        self.runFrame.grid(column=0, row=0)

        self.channelFrame = Frame(self.root)
        self.channelFrame.grid(column=1, row=1, padx=5)

        self.triggerFrame = Frame(self.root)
        self.triggerFrame.grid(column=2, row=1)

        self.timeFrame = Frame(self.root)
        self.timeFrame.grid(column=0, row=1, padx=5)

        self.waveGenFrame = Frame(self.root)
        self.waveGenFrame.grid(column=3, row=1)

        self.PDEframe = Frame(self.root)
        self.PDEframe.grid(column = 0, row = 4)


        #======================RUN / MES COMMANDS==============================
 
        self.runStopBut = tk.Button(self.runFrame, text="RUN/STOP", command=self.runStopCmd, background="red")
        self.runStopBut.grid(column=0, row=0)

        self.singleBut = tk.Button(self.runFrame, text = "SINGLE", command=lambda: self.thread(self.single))
        self.singleBut.grid(column=1, row=0)


        #======================CHANNEL 1, column 1=============================
        self.chan1 = Channel(self, self.channelFrame, ID = 1)


        #======================CHANNEL 2, column 2 =============================
        self.chan2 = Channel(self, self.channelFrame, ID = 2)

        #=======================TIME============================
        self.timeLabel = Label(self.timeFrame, text = "Time axis "+data.numberToStringConvert(self.timeRang/10)+"s/div")
        self.timeLabel.grid(column=0, row=0)

        self.setTimeDiv = Label(self.timeFrame, text="Set time range")
        self.setTimeDiv.grid(column=0, row=1, pady = 2)
        self.setTentry = Entry(self.timeFrame)
        self.setTentry.grid(column=1, row=1, pady= 2)
        self.setTentry.bind('<Return>', self.setTime)

        #======================TRIGGER==========================0
        self.triggerLabel = Label(self.triggerFrame, text = "Trigger")
        self.triggerLabel.grid(column=0, row=0)

        # Variable to hold the selection, where "Option 1" and "Option 2" are the values
        self.selection_var = tk.StringVar(value="1")

        # Create two ttk.Checkbutton widgets with the same variable
        self.trigChan1 = Checkbutton(self.triggerFrame, text="Channel 1", variable=self.selection_var, 
                                    onvalue="1", offvalue="None", command=self.trigChanSelect)
        self.trigChan2 = Checkbutton(self.triggerFrame, text="Channel 2", variable=self.selection_var, 
                                    onvalue="2", offvalue="None", command=self.trigChanSelect)

        # Position the checkbuttons next to each other
        self.trigChan1.grid(row=1, column=0, padx=10, pady=10)
        self.trigChan2.grid(row=1, column=1, padx=10, pady=10)

        # Create a Spinbox with a range and step size of 10e-3
        self.spinbox = Entry(self.triggerFrame)
        self.spinbox.grid(row=2, column=0, pady=10)
        self.spinbox.bind("<Return>", self.triggerEnter)
        # Custom button for incrementing the value
        self.increment_button = Button(self.triggerFrame, text="▲", command=lambda: self.increment_value(5e-3))
        self.increment_button.grid(row=2, column=1)

        # Custom button for decrementing the value
        self.decrement_button = Button(self.triggerFrame, text="▼", command=lambda: self.increment_value(-5e-3))
        self.decrement_button.grid(row=2, column=2)

        # Set the initial value in scientific notation
        self.spinbox.insert(0, "0.00 V")

        #=======================wAVE GEN========================
        self.waveGenVolt = 2.4
        self.waveGenWidth = 300e-9
        self.waveGenFreq = 500e3
        self.instr.setWaveGen(self.waveGenVolt, self.waveGenWidth, self.waveGenFreq)# Default settings for blue PDE measurements, turns it off
        self.wavGenIsOn = False
        self.wavGenOnBut = tk.Button(self.waveGenFrame, text = "Wave Gen", command = self.waveGenOnOff, background = "#f0f0f0")
        self.wavGenOnBut.grid(column=0, row=0)

        #=======================PDE / Photon counting stuff======================
        self.peakHeightValue = 10e-3
        self.peakHeightLab = Label(self.PDEframe, text = f"Peak height: {self.peakHeightValue}")
        self.peakHeightLab.grid(column=0, row=0)
        self.peakHeightEnt = Entry(self.PDEframe)
        self.peakHeightEnt.grid(column=1, row=0)
        self.peakHeightEnt.bind("<Return>", self.setPeakHeight)

        self.peakDistanceValue = 10
        self.peakDistanceLab = Label(self.PDEframe, text = f"Peak distance: {self.peakDistanceValue}")
        self.peakDistanceLab.grid(column=0, row=1)
        self.peakDistanceEnt = Entry(self.PDEframe)
        self.peakDistanceEnt.grid(column=1, row=1)
        self.peakDistanceEnt.bind("<Return>", self.setPeakDistance)

        self.peakPromValue = 16e-3
        self.peakProminenceLab = Label(self.PDEframe, text = f"Peak prominence: {self.peakPromValue}")
        self.peakProminenceLab.grid(column=0, row=2)
        self.peakProminanceEnt = Entry(self.PDEframe)
        self.peakProminanceEnt.grid(column=1, row=2)
        self.peakProminanceEnt.bind("<Return>", self.setPeakProm)

        self.numberOfDatasetsValue = 100
        self.numberOfDatasetsLab = Label(self.PDEframe, text = f"Number of datasets: {self.numberOfDatasetsValue}")
        self.numberOfDatasetsLab.grid(column=0, row=3)
        self.numberOfDatasetsEnt = Entry(self.PDEframe)
        self.numberOfDatasetsEnt.grid(column=1, row=3)
        self.numberOfDatasetsEnt.bind("<Return>", self.setNumberOfDatasets)

        self.testCountBut = Button(self.PDEframe, text = "Test count", command = self.testCount)
        self.testCountBut.grid(column=2, row=0)
        self.testCountResLab = Label(self.PDEframe, text = "")
        self.testCountResLab.grid(column=3, row=0)

        self.photoDistBut = Button(self.PDEframe, text = "Photon distribution", command = self.photonDistribution)
        self.photoDistBut.grid(column=2, row=1)

        self.photoPlotBut = Button(self.PDEframe, text = "Plot", command = self.plotPhotoDist)
        self.photoPlotBut.grid(column=2, row=2)


    def runStopCmd(self):
        if self.instr.isRunning == True:
            self.runStopBut.config(background = "red")
        elif self.instr.isRunning == False:
            self.runStopBut.config(background = "green")
        self.instr.runStop()

    def single(self):
        self.runStopBut.config(background = "#f0f0f0")
        self.singleBut.config(background = "orange")
        self.instr.singleRun()
        self.runStopBut.config(background = "red")
        self.singleBut.config(background = "#f0f0f0")

#==============TRIGGER COMMANDS=========================

    def trigChanSelect(self):
        self.selected = self.selection_var.get()
        self.instr.setTriggerChannel(self.selected)
        print(f"Trigger channel set to: {self.selected}")

    def triggerValue(self):
        try:
            value_str = self.spinbox.get()
            # Convert input string to float for processing
            if "mV" in value_str:
                value = float(value_str.replace("mV", "").strip()) * 1e-3
            else:
                value = float(value_str.replace("V", "").strip())

            self.instr.setTriggerValue(triggerValue=value)
            formatted_value = data.format_value(value)
            #self.spinbox_var.set(formatted_value)
            self.spinbox.delete(0, tk.END)
            self.spinbox.insert(0, formatted_value)
            print(f"Current value: {formatted_value}")
        
        except ValueError:
            self.spinbox.delete(0, tk.END)
            self.spinbox.insert(0, "0.000 V")
            self.instr.setTriggerValue(triggerValue=0)
            print("Invalid input. Resetting trigger to 0.000 V")


    def triggerEnter(self, event):
        self.triggerValue()
    
    def increment_value(self, increment):
        try:
            # Get the current value and strip the unit
            value_str = self.spinbox.get().replace(" V", "").replace("mV", "").replace("μV", "").replace("nV", "").strip()
            
            # Convert to float based on the current unit
            if "mV" in self.spinbox.get():
                value = float(value_str) * 1e-3
            else:
                value = float(value_str)

            # Increment or decrement the value
            value += increment
            self.instr.setTriggerValue(triggerValue=value)
            formatted_value = data.format_value(value)

            # Update the Spinbox with the new formatted value
            self.spinbox.delete(0, tk.END)
            self.spinbox.insert(0, formatted_value)
            
        except ValueError:
            self.spinbox.delete(0, tk.END)
            self.spinbox.insert(0, "0.000 V")
            self.instr.setTriggerValue(triggerValue=0)
            print("Invalid input. Resetting trigger to 0.000 V")
            
    

#==============Wave gen commands========================
    def waveGenOnOff(self):
        if self.wavGenIsOn == False:
            self.wavGenOnBut.config(background="deepskyblue")
            self.wavGenIsOn = True
            self.instr.command(":WGEN:OUTPut 1")
        elif self.wavGenIsOn == True:
            self.wavGenOnBut.config(background="#f0f0f0")
            self.wavGenIsOn = False
            self.instr.command(":WGEN:OUTPut 0")        
    
#===============Photon counting commands===============
    def setPeakHeight(self, event):
        self.peakHeightValue = float(self.peakHeightEnt.get())
        self.peakHeightEnt.delete(0, tk.END)
        self.peakHeightLab.config(text=f"Peak height: {self.peakHeightValue}")
    
    def setPeakDistance(self, event):
        self.peakDistanceValue = float(self.peakDistanceEnt.get())
        self.peakDistanceEnt.delete(0, tk.END)
        self.peakDistanceLab.config(text = f"Peak distance: {self.peakDistanceValue}")
    
    def setPeakProm(self, event):
        self.peakPromValue = float(self.peakProminanceEnt.get())
        self.peakProminanceEnt.delete(0, tk.END)
        self.peakProminenceLab.config(text = f"Peak prominance: {self.peakPromValue}")
    
    def setNumberOfDatasets(self, event):
        self.numberOfDatasetsValue = int(self.numberOfDatasetsEnt.get())
        self.numberOfDatasetsEnt.delete(0, tk.END)
        self.numberOfDatasetsLab.config(text = f"Number of datasets: {self.numberOfDatasetsValue}")

    def testCount(self):
        peaks = self.instr.photonCountSingle(self.peakHeightValue, self.peakDistanceValue, self.peakPromValue)
        self.testCountResLab.config(text = f"{peaks} peaks detected.")

    def photonDistribution(self):
        photoDist = self.instr.photonCount(self.numberOfDatasetsValue, self.peakHeightValue, self.peakDistanceValue, self.peakPromValue)
        meanPhotons = data.plotPhotonDistribution(photoDist)
        name = data.inputText("csv file name")
        data.photoDistToCSV(name, photoDist, header = f"Wave gen settings: voltage {self.waveGenVolt}, width {self.waveGenWidth}, frequency {self.waveGenFreq}\nPeak finder settings: peak height {self.peakHeightValue}, peak distance {self.peakDistanceValue}, peak prominence {self.peakPromValue}")
        
    def plotPhotoDist(self):
        file = data.ChooseFiles(initdir="./dataCollection" ,text = "Choose photon distribution to plot")
        photoDist = data.CSVtoPhotoDist(file[0])
        data.plotPhotonDistribution(photoDist)


    def setTime(self, event):
        self.timeRang = float(self.setTentry.get())
        self.instr.setTimeRange(self.timeRang)
        self.timeLabel.config(text = "Time axis "+data.numberToStringConvert(self.timeRang / 10)+"s/div")
        self.setTentry.delete(0, "end")

    def thread(self, command):
        threading.Thread(target=command).start()

    def DESTRUCTION(self):
        self.instr.closeResource()
        self.root.quit()



class Channel:
    def __init__(self, parent, parentFrame, ID: int):
        self.channelID = ID
        self.parent = parent

        self.parent.instr.displayOff(self.channelID)
        self.channelOn = 0
        

        self.chanFrame = Frame(parentFrame)
        self.chanFrame.grid(column=ID-1, row=0, padx=5)
        self.row = 0
        self.background = ["yellow", "lightgreen"]
        self.channelLabel = Label(self.chanFrame, text = "Channel "+str(ID), background=self.background[ID-1])
        self.channelLabel.grid(column=0, row = self.row)
        self.row += 1


        #=================Channel ON / OFF button====================================
        self.onOffrow = self.row
        self.chanOnOffbut = tk.Button(self.chanFrame, text = "Channel On/Off", command= self.channelOnOff)
        self.chanOnOffbut.grid(column=0, row=self.onOffrow)
        
        self.row += 1

        #=================Channel voltage scale======================================
        self.voltSpinbox = tk.Spinbox(self.chanFrame, from_=40e-3, to=80, increment=80e-3, format="%.3f", command=self.setVolt)
        self.voltSpinbox.grid(column=0, row =self.row, padx=10, pady=10)
        self.voltSpinbox.bind("<Return>", self.enterPressed)

        self.voltSpinbox.delete(0, tk.END)
        if self.channelID == 1:
            self.voltSpinbox.insert(0, f"{160e-3}")
        elif self.channelID == 2:
            self.voltSpinbox.insert(0, f"{8}")

    
    def setVolt(self):
        try:
            value = float(self.voltSpinbox.get())
            self.voltSpinbox.delete(0, tk.END)
            self.voltSpinbox.insert(0, f"{value:.3e}")
            self.parent.instr.setChannelVolt(self.channelID, value)
        except ValueError:
            self.voltSpinbox.delete(0, tk.END)
            self.voltSpinbox.insert(0, "4")
            self.parent.instr.setChannelVolt(self.channelID, 4)
            print("Invalid input. Resetting to 4")
    
    def enterPressed(self, event):
        self.setVolt()

    def channelOnOff(self):
        if self.channelOn == 0:
            self.parent.instr.displayOn(self.channelID)
            self.channelOn = 1
            self.chanOnOffbut.config(background = self.background[self.channelID-1])
        elif self.channelOn == 1:
            self.parent.instr.displayOff(self.channelID)
            self.channelOn = 0
            self.chanOnOffbut.config(background = "#f0f0f0")




if __name__ == '__main__':
    root = tk.Tk()
    app = DSOX1102GGUI(root)
    root.mainloop()