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
        self.root.title("PDE counting")

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

        self.voltAxVar = tk.IntVar(value = 0)
        self.voltageAxBut = Checkbutton(button_frame, text="Bias voltage", variable=self.voltAxVar, onvalue=0, command = self.updatePlot)
        self.overVoltageAxBut = Checkbutton(button_frame, text="Over voltage", variable=self.voltAxVar, onvalue=1, command = self.updatePlot)
        self.voltageAxBut.grid(column=1, row=0)
        self.overVoltageAxBut.grid(column=2, row=0)

        self.files = []
        
        
        

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.ax2 = self.ax.twinx()
        self.x = np.linspace(0, 2 * np.pi, 100)
        self.lines = []

        # Create a canvas and add the figure to it
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add the Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.main_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Frame to hold the ylim buttons
        sample_frame = Frame(self.main_frame)
        sample_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        Label(sample_frame, text="Y limit min").grid(column=0, row=0)
        Label(sample_frame, text="Y limit max").grid(column=1, row=0)
        self.ylim_min_button = tk.Spinbox(sample_frame, command=self.updatePlot, from_=0, to=20, increment=0.5, wrap=True)
        self.ylim_min_button.delete(0, "end")
        self.ylim_min_button.insert(0, 0)
        self.ylim_min_button.grid(column=0, row=1)
        self.ylim_max_button = tk.Spinbox(sample_frame, command=self.updatePlot, from_=1, to=40, increment=0.5, wrap=True)
        self.ylim_max_button.delete(0, "end")
        self.ylim_max_button.insert(0, 9)
        self.ylim_max_button.grid(column=1, row=1)
        


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
        self.ax2.clear()
        ylim1 = float(self.ylim_min_button.get())
        ylim2 = float(self.ylim_max_button.get())
        self.ax.set_ylim(ylim1,ylim2)

        if self.voltAxVar.get() == 0:
            #print("X axis = bias voltage")
            for file in self.files:
                
                if file.isPDEref == True:
                    if file.PDErefVar.get() == 1:
                        """BLUE. Using relative PDE and PDE value for 27 V at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*0.31, ylim2 / float(file.meanPhotoDict[file.refKey])*0.31)
                        referencePDEvalue = 0.31
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key) for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey), file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("Blue ref (Onsemi)")
                    if file.PDErefVar.get() == 0:
                        self.ax2.get_yaxis().set_visible(False)
                        print("No ref")
                    if file.PDErefVar.get() == 2:
                        """UV. Using relative PDE and PDE value for 27 V at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*0.08, ylim2 / float(file.meanPhotoDict[file.refKey])*0.08)
                        referencePDEvalue = 0.08
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key) for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey), file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("UV ref (Onsemi)")
                    if file.PDErefVar.get() == 3:
                        """BLUE. Using relative PDE and PDE value for 4 overvoltage at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        referencePDEvalue = 0.29
                        # Different protocol for hamamatsu
                        file.relPDEdict, file.refKey = data.relativePDEdict(file.meanPhotoDict, False, bdVolt=file.bdVoltValue)

                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue, ylim2 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue)
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key) for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey), file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("Blue ref (Hamamatsu)")
                    if file.PDErefVar.get() == 4:
                        """UV. Using relative PDE and PDE value for 4 overvoltage at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        referencePDEvalue = 0.17
                        # Different protocol for hamamatsu
                        file.relPDEdict, file.refKey = data.relativePDEdict(file.meanPhotoDict, False, bdVolt=file.bdVoltValue)

                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue, ylim2 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue)
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key) for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey), file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("Blue ref (Hamamatsu)")

                meanPhotoDictKeys = [float(key) for key in file.meanPhotoDict.keys()]
                self.ax.scatter(meanPhotoDictKeys, file.meanPhotoDict.values(), color = file.color, marker="x", label = f"{file.name}")
                self.ax.set_ylabel("Mean number of photons")
            self.ax.set_xlabel("Bias voltage / V")

        elif self.voltAxVar.get() == 1:
            #print("X axis = over voltage")
            for file in self.files:
                Vbr = file.bdVoltValue

                if file.isPDEref == True:
                    if file.PDErefVar.get() == 1:
                        """Using relative PDE and PDE value for 27 V at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*0.31, ylim2 / float(file.meanPhotoDict[file.refKey])*0.31)
                        referencePDEvalue = 0.31
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key)-Vbr for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey)-Vbr, file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("Blue ref")
                    if file.PDErefVar.get() == 0:
                        self.ax2.get_yaxis().set_visible(False)
                        print("No ref")
                    if file.PDErefVar.get() == 2:
                        """UV. Using relative PDE and PDE value for 27 V at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*0.08, ylim2 / float(file.meanPhotoDict[file.refKey])*0.08)
                        referencePDEvalue = 0.08
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key)-Vbr for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey)-Vbr, file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("UV ref")
                    if file.PDErefVar.get() == 3:
                        """BLUE. Using relative PDE and PDE value for 4 overvoltage at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        referencePDEvalue = 0.29
                        # Different protocol for hamamatsu
                        file.relPDEdict, file.refKey = data.relativePDEdict(file.meanPhotoDict, False, bdVolt=file.bdVoltValue)

                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue, ylim2 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue)
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key)-Vbr for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey)-Vbr, file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("Blue ref (Hamamatsu)")
                    if file.PDErefVar.get() == 4:
                        """UV. Using relative PDE and PDE value for 4 overvoltage at room temperature given by manufactorer, plots the PDE on second axis"""
                        self.ax2.get_yaxis().set_visible(True)
                        referencePDEvalue = 0.17
                        # Different protocol for hamamatsu
                        file.relPDEdict, file.refKey = data.relativePDEdict(file.meanPhotoDict, False, bdVolt=file.bdVoltValue)
                        
                        self.ax2.set_ylim(ylim1 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue, ylim2 / float(file.meanPhotoDict[file.refKey])*referencePDEvalue)
                        absolutePDEvalues = [relPDE * referencePDEvalue for relPDE in file.relPDEdict.values()]
                        relPDEdictKeys = [float(key)-Vbr for key in file.relPDEdict.keys()]
                        self.ax2.scatter(relPDEdictKeys, absolutePDEvalues, color = file.color, marker="x", label = f"{file.name}")
                        self.ax2.scatter(float(file.refKey)-Vbr, file.relPDEdict[file.refKey]*referencePDEvalue, s=80, facecolors='none', edgecolors=file.color, label="Reference point")
                        #self.ax2.set_ylabel("PDE")
                        print("Blue ref (Hamamatsu)")


                meanPhotoDictKeys = [float(key)-Vbr for key in file.meanPhotoDict.keys()]
                self.ax.scatter(meanPhotoDictKeys, file.meanPhotoDict.values(), color = file.color, marker="x", label = f"{file.name}")
                self.ax.set_ylabel("Mean number of photons")
            self.ax.set_xlabel("Over voltage / V")
            
        self.ax.legend(loc = "upper left")
            

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
        self.isPDEref = False
        self.bdVoltValue = 0
        

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
        # PDE ref frame
        self.pdeRef_frame = Frame(self.frame)
        self.pdeRef_frame.grid(row = 1, column = 0)

        # List to hold file entries
        self.files = []


        
        # Select plot color
        self.colorButton = tk.Button(self.button_frame, text="Color", command=self.choose_color)
        self.colorButton.grid(row=0, column=0, padx=5)

        # Plot relativePDE / mean number of photons
        self.pdeRefLab = Label(self.pdeRef_frame, text = "Use as PDE reference point")
        self.pdeRefLab.grid(row=0, column=0)
        self.uselessVar = tk.IntVar(value=0) # Get rid of dark box
        self.pdeRefBut = Checkbutton(self.pdeRef_frame, command=self.useAsRefPDE, variable=self.uselessVar)
        self.pdeRefBut.grid(row=0, column=1)

        self.PDErefVar = tk.IntVar(value = 0) # 0 non, 1 blue Onsemi, 2 uv Onsemi
        #self.plotRelPDEButton = Checkbutton(self.pdeRef_frame, text = f"None", command=self.relativePDEplot, variable = self.PDErefVar, onvalue=0)
        #self.plotRelPDEButton.grid(row = 1, column = 0)
        self.plotRelBluePDEButton = Checkbutton(self.pdeRef_frame, text = f"Blue Onsemi", command=self.relativePDEplot, variable = self.PDErefVar, onvalue=1)
        self.plotRelBluePDEButton.grid(row = 1, column = 1)
        self.RelPDEuvButton = Checkbutton(self.pdeRef_frame, text = f"UV Onsemi", command=self.relativePDEplot, variable = self.PDErefVar, onvalue=2)
        self.RelPDEuvButton.grid(row=1, column=2)
        self.plotRelBluePDEButtonHama = Checkbutton(self.pdeRef_frame, text = f"Blue Hama", command=self.relativePDEplot, variable = self.PDErefVar, onvalue=3)
        self.plotRelBluePDEButtonHama.grid(row = 2, column = 1)
        self.RelPDEuvButtonHama = Checkbutton(self.pdeRef_frame, text = f"UV Hama", command=self.relativePDEplot, variable = self.PDErefVar, onvalue=4)
        self.RelPDEuvButtonHama.grid(row=2, column=2)

        
        # Rename file (and plot label)
        self.renameBut = Button(self.button_frame, text = "Rename file", command=self.rename)
        self.renameBut.grid(row=0, column=3, padx=5)

        # Delete file from plot
        self.showhide_button = Button(self.button_frame, text="Delete", command=self.killSelf)
        self.showhide_button.grid(row=0, column=4, padx=5)

        # Manually enter breakdown voltage
        self.bdVlab = Label(self.button_frame, text = "Vbr: "+str(self.bdVoltValue))
        self.bdVlab.grid(row=0, column=1)
        self.bdVentry = Entry(self.button_frame)
        self.bdVentry.bind("<Return>", self.enterPressed)
        self.bdVentry.grid(row=0, column=2)

    
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

    def enterPressed(self, event):
        self.setBreakdown()

    def setBreakdown(self):
        bdV = float(self.bdVentry.get())
        self.bdVentry.delete(0, tk.END)
        self.bdVoltValue = bdV
        self.bdVlab.config(text = "Vbr: "+str(self.bdVoltValue))
        self.parent.updatePlot()

    def useAsRefPDE(self):
        if self.isPDEref == False:
            self.isPDEref = True
        elif self.isPDEref==True:
            self.isPDEref = False

    def relativePDEplot(self):
        
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