import tkinter as tk
from tkinter.ttk import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

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
        tempPaths = data.ChooseFiles(initdir="./dataCollection")
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
        self.xMin, self.xMax = 0, 0
        for file in self.files:
            voltList = file.getVoltList()
            if file.getIsSqrt() == False:
                curList = file.getCurrList()
            if file.getIsSqrt() == True:
                curList = file.getSqrtCurList()
            for volt in voltList:
                if volt < self.xMin:
                    self.xMin = volt
                if volt > self.xMax:
                    self.xMax = volt
            self.ax.scatter(voltList, curList, color = file.getColor())
            

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
    def __init__(self, parent, pathName: str, parentFrame, id = 0):
        self.parent = parent
        self.id = id
        self.name = pathName.split("/")[-1]
        self.color = "red"

        # Reads the data and saves it as float lists
        self.voltList, self.curList = data.readIVsweepFile(pathName)
        self.sqrtCurList = [np.sqrt(max(cur,0)) for cur in self.curList]
        self.isSqrt = False


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


        # Available colors for the dropdown
        colors = ["Red", "Green", "Blue", "Yellow", "Black", "White"]

        # Variable to hold the selected color
        selected_color = tk.StringVar()

        # Creating the button
        self.colorButton = tk.Menubutton(self.button_frame, text="Select Color", direction="below")
        self.colorButton.grid(row=0, column=0, padx=5)

        # Creating the menu and adding color options
        self.menu = tk.Menu(self.colorButton, tearoff=0)
        """ for color in colors:
            self.menu.add_radiobutton(label=color, variable=selected_color, value=color, command=lambda: self.select_color(selected_color.get())) """

        for color in colors:
            self.menu.add_command(
                label=color,
                background=color,  # Set the background to the color
                activebackground=color,  # Set the active background to the color
                command=lambda c=color: self.select_color(c)  # Pass the color value to the function
    )

        self.colorButton["menu"] = self.menu


        
        self.SqrtButton = Checkbutton(self.button_frame, text = f"Square root", command=self.squareRoot)
        self.SqrtButton.grid(row = 0, column = 1)

        self.showhide_button = Button(self.button_frame, text="Delete", command=self.killSelf)
        self.showhide_button.grid(row=0, column=2, padx=5)

    
    def print(self):
        print("Hello")

    def getColor(self):
        return self.color
    def setColor(self, color):
        self.color = color
    def getVoltList(self):
        return self.voltList
    def getCurrList(self):
        return self.curList
    def getSqrtCurList(self):
        return self.sqrtCurList
    def getIsSqrt(self):
        return self.isSqrt
    
    def squareRoot(self):
        if self.isSqrt == False:
            self.isSqrt = True
        else:
            self.isSqrt = False
        self.parent.updatePlot()
    
    def select_color(self, value):
        self.colorButton.config(text=f"{value}", background = value)
        self.color = value
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