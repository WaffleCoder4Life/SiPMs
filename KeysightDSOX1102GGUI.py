from Devices import DSOX1102G
from tkinter.ttk import *
import tkinter as tk


class DSOX1102GGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DSOX1102G")

        self.root.protocol('WM_DELETE_WINDOW', self.DESTRUCTION) # pressing 'x' closes


        # Create DSOX1102G object
        self.instr = DSOX1102G()

        
        #self.chan2 = Channel(2)



        


        #======================CHANNEL 1 FRAME=============================
        self.chan1 = Channel(self, self.root, ID = 1)

        #======================CHANNEL 2 FRAME=============================

    


    def DESTRUCTION(self):
        self.instr.closeResource()
        self.root.quit()



class Channel:
    def __init__(self, parent, parentFrame, ID: int):
        self.channelID = ID
        self.channelOn = 0
        self.parent = parent

        self.chanFrame = Frame(parentFrame)
        self.chanFrame.grid(column=ID-1, row=0)

        self.chanOFFbut = Button(self.chanFrame, text = "Channel Off", command=lambda: self.channelOnOff)
        self.chanOFFbut.grid(column=0, row=0)
        self.chanOFFbut.grid_remove()

        self.chanONbut = Button(self.chanFrame, text = "Channel On", command=self.channelOnOff)
        self.chanONbut.grid(column=0, row=0)

    
    

    def channelOnOff(self):
        if self.channelOn == 0:
            self.parent.instr.displayOn(self.channelID)
            self.channelOn = 1
            self.chanONbut.grid_remove()
            self.chanOFFbut.grid(column=0, row=0)
        if self.channelOn == 1:
            self.parent.instr.displayOff(self.channelID)
            self.channelOn = 0
            self.chanOFFbut.grid_remove()
            self.chanONbut.grid(column=0, row=0)




if __name__ == '__main__':
    root = tk.Tk()
    app = DSOX1102GGUI(root)
    root.mainloop()