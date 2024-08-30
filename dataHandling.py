import os
import tkinter as tk
import json
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from typing import Tuple
from tkinter import *
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import *
from collections import Counter
import pandas as pd
import json

#=========================================FOLDER HANDLING============================================================================

def ChooseFolder(initdir = "..", title = ""):
    """Open folder window to choose a folder. Returns folder path."""
    # Initialise tkinter window
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    
    # Prompt to choose the files to process.
    datafolder = filedialog.askdirectory(initialdir = initdir, title = title, parent = root)
    
    root.destroy()
    return datafolder

def nameIsTaken(path, name):
    """Check if file name is taken. Return true (taken) or false (not taken)"""
    if os.path.isfile(path+"/"+name):
        print("Filename taken (csv)")
        return True
    else:
        return False
    
def inputText(title):
    """Window to input text in."""
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.tk.eval(f'tk::PlaceWindow {root._w} center')
    root.withdraw()
    return simpledialog.askstring(title, f"Enter {title} below:")

def ChooseFileMultiple(initdir = "..", text = 'Choose files', filetypes = [('csv files', '*.csv')]) -> Tuple[list, str]:
    """Choose a csv file and ask wether to add more files. Returns tuple[list, string] where string = 'yes' or 'no'."""
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.tk.eval(f'tk::PlaceWindow {root._w} center')
    root.withdraw()
    files = filedialog.askopenfilenames(initialdir = initdir,title=text, filetypes = filetypes)
    msgbox = messagebox.askquestion ('Add files','add extra files',icon = 'warning')
    return list(files), msgbox

def ChooseFilesDifferentFolders(initdir = "..", text = "Choose files", filetypes = [('csv files', '*.csv')]):
    """Choose csv files from different folders. Returns all selected file paths as a list."""
    files, msbox = ChooseFileMultiple(initdir=initdir, text = text, filetypes = filetypes)
    allFiles = files
    while msbox == "yes":
        files2, msbox = ChooseFileMultiple(initdir = initdir, text = text, filetypes = filetypes)
        for file in files2:
            allFiles.append(file)
    return allFiles

def ChooseFiles(initdir = "..", text = 'Choose files', filetypes = [('csv files', '*.csv')]) -> Tuple[list, str]:
    """Choose a csv file and ask wether to add more files. Returns tuple[list, string] where string = 'yes' or 'no'."""
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.tk.eval(f'tk::PlaceWindow {root._w} center')
    root.withdraw()
    files = filedialog.askopenfilenames(initialdir = initdir,title=text, filetypes = filetypes)
    return list(files)

def returnToday():
    today = date.today()
    day = "{:02d}".format(today.day)
    month = "{:02d}".format(today.month)
    return day + month + str(today.year)


#====================================OSCILLOSCOPE STUFF===========================================================


def photoDistToCSV(name, photoCountData, header="", path="./dataCollection"):
    fileName = returnToday() + name +"1"
    i = 1
    while nameIsTaken(path, fileName+".csv"):
        fileName = fileName[:-1]
        fileName += str(i)
        i += 1
    np.savetxt(path+"/"+fileName+".csv", photoCountData, header=header, delimiter=",")

def CSVtoPhotoDist(pathToFile):
    return np.genfromtxt(pathToFile, delimiter=",")

def saveOscilloImage(path, name, data):
    f = open(f"{path}/{name}.png", "wb")
    f.write(data)
    f.close()

def oscilloPeakCounter(voltData, peakHeight, distance, prominence):
    peaks = find_peaks(voltData, height = peakHeight, distance = distance, prominence=prominence)
    print(peaks[0])
    print(f"{len(peaks[0])} fotons detected")
    return len(peaks[0])

def peakCounter(voltData, peakHeight, distance, prominence, useOriginal = False):
    """Modified peak counter to only use left hand sided prominence for filtering peaks."""
    if useOriginal:
        fotons = oscilloPeakCounter(voltData, peakHeight, distance, prominence)
        #print(f"Original peak counter used")
    else:
        peaks, _ = find_peaks(voltData, height = peakHeight, distance = distance, prominence=0)
        _ , left_bases, _ = peak_prominences(voltData, peaks)
        left_prominences = []
        #print(f"Peaks before filter: {peaks}")
        #print(f"Left bases: {left_bases}")
        for i in range(len(peaks)):
            left_prominences.append(voltData[peaks[i]] - voltData[left_bases[i]])
        fotons = 0
        truePeaks = []
        leftProm = []
        truePeakProm = []
        for i in range(len(left_prominences)):
            if left_prominences[i] > prominence:
                fotons += 1
                truePeaks.append(peaks[i])
                leftProm.append(left_bases[i])
                truePeakProm.append(left_prominences[i])
        print(f"{fotons} fotons detected")
        print(f"Peak locatins {truePeaks}")
        #print(f"Left base locations {leftProm}")
        #print(f"Peak LHS prominences {truePeakProm}")

        
    return fotons

def afterPulseCounter(voltData, peakHeight, distance, prominence, pulseMax):
    """Records 5us before and after dark count. Only counts afterpulses if 5 us prior to trigger is empty of peaks."""
    if max(voltData[9950:10050]) > pulseMax:
        print("Max limit reached")
        return None
    if min(voltData) < -0.0015:
        print("Random noise appeared")
        return None

    peaks, _ = find_peaks(voltData, height = peakHeight, distance = distance, prominence=0)
    _ , left_bases, _ = peak_prominences(voltData, peaks)
    left_prominences = []
    #print(f"Peaks before filter: {peaks}")
    #print(f"Left bases: {left_bases}")


    for i in range(len(peaks)):
        promHeight = voltData[peaks[i]] - voltData[left_bases[i]]
        left_prominences.append(promHeight)
        if peaks[i] < 9950 and promHeight > prominence:
            print("Peaks prior to trigger appeared")
            return None
    fotons = 0
    truePeaks = []
    leftProm = []
    truePeakProm = []
    for i in range(len(left_prominences)):
        if left_prominences[i] > prominence:
            fotons += 1
            truePeaks.append(peaks[i])
            leftProm.append(left_bases[i])
            truePeakProm.append(left_prominences[i])
    print(f"{fotons} fotons detected")
    print(f"Peak locations {truePeaks}")
    #print(f"Left base locations {leftProm}")
    #print(f"Peak LHS prominences {truePeakProm}")
    return fotons


def peakCounterSout(voltData, peakHeight, distance, prominence, rightProminence = 0.0008, useOriginal = False):
    """Modified peak counter for slow output, use left and right hand sided prominences with different scale. RHS prominance hardcoded for liquid nitrogen."""
    if useOriginal:
        fotons = oscilloPeakCounter(voltData, peakHeight, distance, prominence)
        print(f"Original peak counter used")
    else:
        peaks, _ = find_peaks(voltData, height = peakHeight, distance = distance, prominence=0)
        _ , left_bases, right_bases = peak_prominences(voltData, peaks)
        left_prominences = []
        right_prominences = []
        print(f"Peaks before filter: {peaks}")
        print(f"Left bases: {left_bases}")
        for i in range(len(peaks)):
            left_prominences.append(voltData[peaks[i]] - voltData[left_bases[i]])
            right_prominences.append(voltData[peaks[i]] - voltData[right_bases[i]])
        fotons = 0
        truePeaks = []
        leftProm = []
        truePeakProm = []
        for i in range(len(left_prominences)):
            if left_prominences[i] > prominence and right_prominences[i] > rightProminence:
                fotons += 1
                truePeaks.append(peaks[i])
                leftProm.append(left_bases[i])
                truePeakProm.append(left_prominences[i])
        print(f"{fotons} fotons detected")
        print(f"Peak locatins {truePeaks}")
        print(f"Left base locations {leftProm}")
        print(f"Peak LHS prominences {truePeakProm}")

        
    return fotons



def plotPhotonDistribution(photonDistribution, plotShow = True):
    """Plots the poissonian distribution for mean number of photons in the pulse and the measured data."""
    photonCounts = Counter(photonDistribution) 
    print(photonCounts)

    # Counts mean number of photons in photonDistribution
    poisson_lambda = 0
    for key in photonCounts:
        poisson_lambda += int(key)*int(photonCounts[key])
    poisson_lambda /= len(photonDistribution)
    print(f"Mean value of photons {poisson_lambda}")

    poisdata = np.random.poisson(poisson_lambda, 10000*len(photonDistribution)) #Create a distribution for counted mean number of photons

    labels, counts = np.unique(photonDistribution, return_counts=True)
    plt.bar(labels, counts, width = 1, color = "darkorange", edgecolor = "black", align='center', linestyle = "--", label = "measurement")
    plotLabels = [point for point in range(-1, int(labels[-1]+1), 1)]
    plt.gca().set_xticks(plotLabels)
    
    labels2, counts2 = np.unique(poisdata, return_counts=True)
    counts2 = [point/10000 for point in counts2[:18]]
    labels2 = [point for point in range(-1, len(counts2), 1)]
    counts2.insert(0, 0)
    plt.step(labels2, counts2, "k", linewidth = 1, where = "mid", label = "Poissonian fit $\\mathrm{\\lambda}$="+str(poisson_lambda))
    
    plt.xlabel("photoelectron")
    plt.ylabel("counts")
    plt.legend()
    plt.xlim(-0.5, int(labels[-1])+1)
    if plotShow:
        plt.show()
    return poisson_lambda

def createPhotonsDict():
    """Counts the mean number of photons (lambda) from each photon distribution. Saves them to dictionary with bias voltage as key and lambda as value.
    Keys are typed in manually. Returns the dictionary sorted by key values (bias voltages)."""
    filePaths = ChooseFiles(initdir="./dataCollection", text = "Choose distributions to count mean number of photons")
    meanPhotonsDict = {}
    for file in filePaths:
        photoDist = CSVtoPhotoDist(file)
        photonCounts = Counter(photoDist)
        # Counts mean number of photons in photonDistribution
        poisson_lambda = 0
        for key in photonCounts:
            poisson_lambda += int(key)*int(photonCounts[key])
        poisson_lambda /= len(photoDist)
        biasVoltage = str(inputText(title=f"Enter BIAS VOLTAGE for file {file[-18:-3]}"))
        meanPhotonsDict[biasVoltage] = poisson_lambda
    meanPhotonsDict = dict(sorted(meanPhotonsDict.items()))
    print(meanPhotonsDict)
    return meanPhotonsDict

def afterPulseProb(distDict):
    keys = list(distDict.keys())
    afterCount = 0
    for i in range(len(keys)-1):
        afterCount += distDict[keys[i+1]]*int(keys[i])
    print(f"{sum(distDict.values())} photons with {afterCount} after pulses")
    return afterCount / sum(distDict.values())


def createPhotonsDictAfterPulseCompensated():
    """UNFINISHED!! Counts the mean number of photons (lambda) from each photon distribution. Saves them to dictionary with bias voltage as key and lambda as value.
    Keys are typed in manually. Returns the dictionary sorted by key values (bias voltages)."""
    filePaths = ChooseFiles(initdir="./dataCollection", text = "Choose distributions to count mean number of photons")
    meanPhotonsDict = {}
    for file in filePaths:
        photoDist = CSVtoPhotoDist(file)
        photonCounts = Counter(photoDist)
        afterPcounts = Counter(CSVtoPhotoDist(filePaths = ChooseFiles(initdir="./dataCollection", text = f"Choose afterpulse dist for {file[-18:-3]}")[0]))
        afterPprob = afterPulseProb(afterPcounts)
        # Counts mean number of photons in photonDistribution
        poisson_lambda = 0
        for key in photonCounts:
            poisson_lambda += int(key)*int(photonCounts[key])*(1-afterPprob)
        poisson_lambda /= len(photoDist)
        biasVoltage = str(inputText(title=f"Enter BIAS VOLTAGE for file {file[-18:-3]}"))
        meanPhotonsDict[biasVoltage] = poisson_lambda
    meanPhotonsDict = dict(sorted(meanPhotonsDict.items()))
    print(meanPhotonsDict)
    return meanPhotonsDict



def writeDictJson(dictionary, initdir = "./dataCollection"):
    """Save a dictionary to json file"""
    fileName = inputText(title="FILE NAME")
    with open(initdir + "/" + fileName+".json", "w") as file:
        json.dump(dictionary, file)

def readDictJson(initdir = "./dataCollection", filePath = None):
    """Choose a SINGLE json file to open and returns a dictionary."""
    if filePath is not None:
        with open(filePath, "r") as f:
            dicti = json.load(f)
        return dicti
    else:
        file = ChooseFiles(initdir=initdir, text = "Choose a json file", filetypes=(("Json File", "*.json"),))[0]
        with open(file, "r") as f:
            dicti = json.load(f)
        return dicti

def relativePDEdict(meanPhotosDict):
    """Calculate relative PDE from mean number of photons. Uses the smallest photon count as the reference point for relative PDE.
    Argument: dict[voltage] = lambda. Returns dict[voltage] = relativePDE dictionary and the key for the reference point."""
    lowLambda = 1000
    refKey = None
    relPDEdict = {}
    for key in meanPhotosDict:
        if meanPhotosDict[key] < lowLambda:
            lowLambda = meanPhotosDict[key]
            refKey = key
    if lowLambda == 100:
        print("Something went wrong")
        return None
    for key in meanPhotosDict:
        relativePDE = meanPhotosDict[key] / lowLambda
        relPDEdict[key] = relativePDE
    return relPDEdict, refKey

#===========================================IV sweep data handling======================================================================================



def IVscatter(voltList, curList, color):
    "Simple plot to check IV curve"
    plt.scatter(voltList, curList, s=10, marker='s', color=color)
    plt.show()

def saveIVscatter(voltList, curList):
    folder = ChooseFolder(initdir="./dataCollection",title="Save to folder...")
    fileName = inputText(title="file name")
    while nameIsTaken(folder, fileName):
        print("Filename taken!")
        folder = ChooseFolder(initdir="./dataCollection",title="Save to folder...")
        fileName = inputText(title="file name")
    with open(folder+"/"+fileName+".csv", "w") as file:
        for i in range(len(voltList)):
            file.write(str(voltList[i])+";"+str(curList[i])+"\n")


def readIVsweepFile(filePath):
    """Opens a CSV file, unpacks the voltage and current readings and returns them as separete float lists."""
    voltageList = []
    currentList = []
    with open(filePath, "r") as file:
        for row in file:
            row.strip("\n")
            rowAsList = row.split(";")
            voltageList.append(float(rowAsList[0]))
            currentList.append(float(rowAsList[1]))
    return voltageList, currentList



def derivative(xdata, ydata):
    derivatives = []
    x = 0
    while x < len(xdata)-1:
        #print(ydata[x+1]-ydata[x])
        #print(xdata[x+1]-xdata[x])
        der = (ydata[x+1]-ydata[x]) / (xdata[x+1]-xdata[x])
        derivatives.append(der)
        x += 1
    return derivatives


# Chat GPT generated stuff to pick a point
class PointPicker:
    def __init__(self, x, y, selection):
        self.x = x
        self.y = y
        self.selected_index = None
        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter(x, y)
        self.ax.set_title(selection)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        
        # Calculate the distances between the click and all points
        distances = np.hypot(self.x - event.xdata, self.y - event.ydata)
        self.selected_index = np.argmin(distances)
        
        print(f'Selected point index: {self.selected_index}')
        plt.close(self.fig)  # Close the plot window

def pick_point_from_scatter(x, y, title):
    picker = PointPicker(x, y, title)
    return picker.selected_index


#=========================USEFUL STUFF================================

def numberToStringConvert(value):
    niceStr = ""
    if 1e-3 <= value < 1:
        niceStr = str(value * 1e3) + "m"
    if 1e-6 <= value <1e-3:
        niceStr = str(value * 1e6) + u"\u03bc"
    if 1e-9 <= value <1e-6:
        niceStr = str(value*1e9) + "n"
    return niceStr


# Function to format the value with appropriate units
def format_value(value):
    if abs(value) >= 1:
        return f"{value:.3f} V"  # Display as Volts for values >= 1 V
    elif abs(value) >= 1e-3:
        return f"{value*1e3:.3f} mV"  # Display as millivolts for values >= 1e-3 V and < 1 V
    elif abs(value) >= 1e-6:
        return f"{value*1e6:.3f} μV"  # Display as microvolts for values >= 1e-6 V and < 1e-3 V
    elif abs(value) >= 1e-9:
        return f"{value*1e9:.3f} nV"  # Display as nanovolts for values >= 1e-9 V and < 1e-6 V
    else:
        return f"{value:.3e} V"  # Display as scientific notation for very small values
