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

def saveOscilloImage(path, name, data):
    f = open(f"{path}/{name}.png", "wb")
    f.write(data)
    f.close()
