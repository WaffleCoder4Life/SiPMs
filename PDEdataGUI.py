import tkinter as tk
from tkinter.ttk import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import scipy.optimize
from sympy import Symbol
from sympy.solvers import solve
from tkinter import colorchooser

import dataHandling as data


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("IV-sweep data analyz")

        # Bind the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        

        # Create a main frame
        self.main_frame = Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create a sidebar frame
        self.sidebar = Frame(root, width=200)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame to hold the add and remove buttons
        button_frame = Frame(self.sidebar)
        button_frame.pack(pady=5)




        # Scrollable canvas for parameters
        self.paramcanvas = tk.Canvas(self.sidebar, borderwidth=0)
        self.scrollbar = Scrollbar(self.sidebar, orient="vertical", command=self.paramcanvas.yview)

        self.parameters_frame = Frame(self.paramcanvas)
        self.parameters_frame.bind("<Configure>", self.on_frame_configure)
        self.paramcanvas.create_window((0, 0), window=self.parameters_frame, anchor="nw")
        self.paramcanvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.paramcanvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.updateFlag = tk.IntVar(value=0)

        #=============================File selection===========================================
        self.filePathList = [] # Store file paths
        self.fileID = 0 # To keep count on files
        self.selectFilesBut = Button(button_frame, text="Add files", command = self.selectFiles)
        self.selectFilesBut.grid(column=0, row=0)

        self.files = []
        
        
        

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.x = np.linspace(0, 2 * np.pi, 100)
        self.lines = []

        # Create a canvas and add the figure to it
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add the Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.main_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Frame to hold the sample control
        sample_frame = Frame(self.main_frame)
        sample_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        Label(sample_frame, text="Number of Samples:").pack(side=tk.LEFT, padx=5)
        self.sample_var = tk.IntVar(value=100)
        self.sample_entry = Entry(sample_frame, textvariable=self.sample_var)
        self.sample_entry.pack(side=tk.LEFT, padx=5)


    def selectFiles(self):
        tempPaths = data.ChooseFiles(initdir="./dataCollection", filetypes=(("json file", "*.json"),))
        for path in tempPaths:
            idTemp = len(self.files)
            new_file = File(self, path, self.parameters_frame, id = idTemp)
            self.files.append(new_file)
        self.updatePlot()
    
    def deleteFile(self, id):
        file = self.files.pop(id)
        file.frame.destroy()
        del file
        # Renumber and reposition the parameters
        for i, optLine in enumerate(self.files):
            optLine.updateID(id = i)
        self.updatePlot()
      
    def updatePlot(self):
        self.ax.clear()
        for file in self.files:
            if file.plotRelPDE == True:
                relPDEdictKeys = [float(key) for key in file.relPDEdict.keys()]
                plt.scatter(relPDEdictKeys, file.relPDEdict.values(), color = file.color, marker="x", label = f"{file.name}")
                plt.scatter(float(file.refKey), file.relPDEdict[file.refKey], s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                self.ax.set_ylabel("Relative PDE")
            elif file.plotRelPDE == False:
                meanPhotoDictKeys = [float(key) for key in file.meanPhotoDict.keys()]
                plt.scatter(meanPhotoDictKeys, file.meanPhotoDict.values(), color = file.color, marker="x", label = f"{file.name}")
                self.ax.set_ylabel("Mean number of photons")
        self.ax.set_xlabel("Bias voltage")
        
        self.ax.legend()
            

        self.canvas.draw()




    def on_frame_configure(self, event):
        self.paramcanvas.configure(scrollregion=self.paramcanvas.bbox("all"))

    def on_closing(self):
        # Properly close the Matplotlib figure
        plt.close(self.fig)
        self.root.quit()

    def savestate(self):
        # Save the state of the GUI in dict for loading
        pass

    def loadstate(self):
        # Load the state of the GUI from a dict
        pass

class File:
    """Create a object from json file"""
    def __init__(self, parent, pathName: str, parentFrame, id = 0):
        self.parent = parent
        self.id = id
        self.name = pathName.split("/")[-1][:-5]
        self.color = "red"
        self.plotRelPDE = False

        # Reads the data and saves it as dict
        self.meanPhotoDict = data.readDictJson(filePath=pathName)
        self.relPDEdict, self.refKey = data.relativePDEdict(self.meanPhotoDict)
        


        self.frame = LabelFrame(parentFrame, text = f"{self.name}")
        self.frame.grid(row=id, column=0, pady=5, sticky="news")
        # Make the frame expand to fill the parent
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        ### BUTTON FRAME ###
        self.button_frame = Frame(self.frame)
        self.button_frame.grid(row=0, column=0, pady=5, sticky="news")
        # Make the frame expand to fill the parent
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

        # List to hold file entries
        self.files = []


        
        # Select plot color
        self.colorButton = tk.Button(self.button_frame, text="Color", command=self.choose_color)
        self.colorButton.grid(row=0, column=0, padx=5)

        # Plot relativePDE / mean number of photons
        self.uselesVar = tk.IntVar(value = 0) # Remove black box
        self.plotRelPDEButton = Checkbutton(self.button_frame, text = f"Relative PDE", command=self.relativePDEplot, variable = self.uselesVar)
        self.plotRelPDEButton.grid(row = 0, column = 1)
        
        
        # Rename file (and plot label)
        self.renameBut = Button(self.button_frame, text = "Rename file", command=self.rename)
        self.renameBut.grid(row=0, column=2, padx=5)

        # Delete file from plot
        self.showhide_button = Button(self.button_frame, text="Delete", command=self.killSelf)
        self.showhide_button.grid(row=0, column=3, padx=5)

    
    def rename(self):
        self.name = data.inputText(title="NEW NAME")
        self.frame.config(text = f"{self.name}")
        self.parent.updatePlot()

    def choose_color(self):
        """Open a color picker dialog and set the color of the given line"""
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.color = color_code[1]
            self.colorButton.config(background = color_code[1])
            self.parent.updatePlot()

    def relativePDEplot(self):
        if self.plotRelPDE == False:
            self.plotRelPDE = True
        else:
            self.plotRelPDE = False
        self.parent.updatePlot()

    def killSelf(self):
        self.parent.deleteFile(self.id)

    def updateID(self, id):
        self.id = id
        # Reposition on grid
        self.frame.grid(row=id, column=0, pady=5, sticky="news")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()