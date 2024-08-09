import matplotlib.pyplot as plt
import dataHandling as data
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class dataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Data analyz")
        self.styleb = Style()
        self.styleb.configure(style='my.TButton', font=('Helvetica', 12))
        self.stylel = Style()
        self.stylel.configure(style='my.TLabel', font=('Helvetica', 12))
        self.root.protocol('WM_DELETE_WINDOW', self.DESTRUCTION) # pressing 'x' closes

        self.filePathList = None

        #=============================FRAMES===================================================
        self.fileFrame = Frame(self.root)
        self.fileFrame.grid(column = 0, row = 0)
        self.plotFrame = Frame(self.root)
        self.plotFrame.grid(column = 1, row = 0)



        #=============================File selection===========================================
        self.selectFilesBut = Button(self.fileFrame, text="Select files", command = self.selectFiles, style = 'my.TButton')
        self.selectFilesBut.grid(column=0, row=0)


        #=============================Plotting==================================================
        # Canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, self.plotFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0)

        # Axis settings
        self.xMin = 0
        self.xMax = 1


        

        self.plotBut = Button(self.plotFrame, text = "Plot", command = self.updatePlot, style = 'my.TButton')
        self.plotBut.grid(column=0, row=1)


    

    def selectFiles(self):
        self.filePathList = data.ChooseFilesDifferentFolders(initdir="./dataCollection")


    
    def updatePlot(self):
        self.ax.clear()
        self.xMin, self.xMax = 0, 0
        for filePath in self.filePathList:
            voltList, curList = data.readIVsweepFile(filePath)
            for volt in voltList:
                if volt < self.xMin:
                    self.xMin = volt
                if volt > self.xMax:
                    self.xMax = volt
            self.ax.scatter(voltList, curList)
        
        self.canvas.draw()



    def DESTRUCTION(self):
        self.root.quit()



if __name__ == '__main__':
    root = Tk()
    app = dataGUI(root)
    root.mainloop()