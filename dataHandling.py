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

def saveOscilloImage(path, name, data):
    f = open(f"{path}/{name}.png", "wb")
    f.write(data)
    f.close()


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




