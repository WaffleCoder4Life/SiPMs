import pyvisa as visa
import numpy as np
from time import sleep
import dataHandling as data

class pyvisaResource:
    """Parent class for pyvisa properties and connections."""
    def __init__(self):
        self.instr = None
        self.rm = visa.ResourceManager()
        self.aborted = False

    def connectDevice(self, name):
        """General function for connecting devices. Compares given name to the IDN of all available visa connections.
        Names: MODEL 6487 (voltage source), DSO-X 1102G (oscilloscope)"""
        devDict = self.rm.list_resources_info().items()
        for key, value in devDict:
            try:
                tempDev = self.rm.open_resource(f"{key}")
                tempDev.write("*IDN?")
                deviceIDN = tempDev.read()
                #print(deviceIDN)
                if name in deviceIDN:
                    self.instr = self.rm.open_resource(f"{key}")
                    print(f"{name} connected succesfully!")
            except:
                pass
    def getInstr(self):
        return self.instr
    
    def command(self, cmnd):
        """Function to give a general command to instrument. cmnd formalism must be looked up from programming manual."""
        self.instr.write(f"{cmnd}")

    def read(self):
        return self.instr.read()

    def abort(self):
        self.aborted=True
        print("ABORTED!!!")

    def closeResource(self):
        self.instr.close()

class Keithley6487(pyvisaResource):
    def __init__(self):
        # VISA CONNECTIONS
        pyvisaResource.__init__(self)
        self.connectDevice("MODEL 6487")

        #RUN THESE AFTER START OR GET FUCKED
        self.instr.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
        self.instr.write("SYST:ZCH OFF")

        # Initialize values
        self.instr.write(":CURR:RANG 0.001") # Set current range
        self.instr.write(f":SOUR:VOLT:RANG 50")  # Set voltage range
        self.instr.write(":SOUR:VOLT:ILIM 2.5e-3") # Set current limit
        self.instr.write(":FORM:ELEM READ") # CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
        self.instr.write(":FORM:DATA ASCii") # Choose data format


        self.currRange = 0.001
        self.voltRange = 50
        self.currLimit = 25e-3
        self.voltage = 0

        self.isOn = False



    def closeResource(self):
        self.instr.write(":SOUR:VOLT:STAT OFF")
        self.instr.close()

    def powerOn(self):
        self.instr.write(":SOUR:VOLT:STAT ON")
        self.isOn = True
    def powerOff(self):
        self.instr.write(":SOUR:VOLT:STAT OFF")
        self.isOn = False

    def readCurrentASCii(self):
        """Triggers a single measurement and returns the current as a float"""
        self.instr.write(":INIT") # Triggers a measurement
        sleep(0.1)
        self.instr.write(":SENS:DATA?") # Asks for data, only stores one set of data
        sleep(0.1)
        return float(self.instr.read()) # Returns the data read from the device

# ---- Getters and Setters for basic properties ----

    def get_currRange(self):
        self.instr.write(":CURR:RANG?")
        return float(self.instr.read())

    def set_currRange(self, value):
        self.instr.write(":CURR:RANG " + str(value))
        self.currRange = self.get_currRange()

    def get_voltRange(self):
        self.instr.write(":SOUR:VOLT:RANG?")
        return float(self.instr.read())

    def set_voltRange(self, value):
        """Allowed values 10 and 50. If other value is given, sets the value to the next lower allowed value."""
        if value < 50:
            self.instr.write(f":SOUR:VOLT:RANG 10")
        elif 50 <= value:
            self.instr.write(f":SOUR:VOLT:RANG 50")
        elif 500 <= value:
            self.instr.write(f":SOUR:VOLT:RANG 500")
        self.voltRange = self.get_voltRange()

    def get_currLimit(self):
        self.instr.write(":SOUR:VOLT:ILIM?")
        return float(self.instr.read())

    def set_currLimit(self, value):
        """Allowed values are 25uA, 250uA and 2.5mA. If some other values is given sets the value to the next lower
        allowed value."""
        if value < 250E-6:
            self.instr.write(":SOUR:VOLT:ILIM 25e-6")
        elif 250E-6 <= value < 2.5E-3:
            self.instr.write(":SOUR:VOLT:ILIM 250e-6")
        elif 2.5E-3 <= value:
            self.instr.write(":SOUR:VOLT:ILIM 2.5e-3")
        self.currLimit = self.get_currLimit()

    def get_voltage(self):
        self.instr.write(":SOUR:VOLT?")
        return float(self.instr.read())

    def set_voltage(self, value):
        self.instr.write(f":SOUR:VOLT {value}")
        self.voltage = self.get_voltage()


    def IVsweep(self, startV, endV, stepV, mesPerV = 1, quickie: bool = False, reverse: bool = False):
        """Perfom IV-sweep from 'startV' to 'endV'. Takes 'mesPerV' measurements every 'stepV' voltage and returns the average current for each voltage.
           Returns the data as two lists; voltage, current. stepV minimum allowed value for 50 V range 0.001 V. Optional parameters; quickie (True/False) overrun 
           stepV and mesPerV for a quick scan with 10 measurement points. Useful for locating breakdown voltage and tuning current limit etc.
           reverse (True/False) to execute the sweep in reverse."""
        if quickie:
            if self.isOn == False:
                self.powerOn()
            voltage = startV
            stepV = (endV - startV) / 10
            currList, voltList = [], []
            self.set_voltage(voltage) #
            self.readCurrentASCii() # These two make sure the first measurement is also correct
            while voltage <= endV:
                self.set_voltage(voltage)
                sleep(0.1)
                voltList.append(voltage)
                currList.append(self.readCurrentASCii())
                voltage += stepV
            self.powerOff()
            return voltList, currList
        else:
            if reverse:
                if self.isOn == False:
                    self.powerOn()
                voltage = endV
                voltList, currList = [], []
                self.set_voltage(voltage) #
                sleep(0.1)
                self.readCurrentASCii() # These two make sure the first measurement is also correct
                while startV <= voltage:
                    if self.aborted:
                        self.aborted = False
                        break
                    self.set_voltage(voltage)
                    sleep(0.5) # sleepy time
                    tempCurr = []
                    for i in range(mesPerV): # loop for average current
                        tempCurr.append(self.readCurrentASCii()) # single current measurement
                        sleep(0.2)
                    currList.append(sum(tempCurr)/(len(tempCurr)))
                    voltList.append(voltage)
                    voltage -= stepV
                currList.reverse()
                voltList.reverse()
                return voltList, currList

            else:
                if self.isOn == False:
                    self.powerOn()
                voltage = startV
                voltList, currList = [], []
                self.set_voltage(voltage) #
                self.readCurrentASCii() # These two make sure the first measurement is also correct
                while voltage <= endV:
                    if self.aborted:
                        self.aborted=False
                        break
                    self.set_voltage(voltage)
                    sleep(0.5) # sleepy time
                    tempCurr = []
                    for i in range(mesPerV): # loop for average current
                        tempCurr.append(self.readCurrentASCii()) # single current measurement
                        sleep(0.2)
                    currList.append(sum(tempCurr)/(len(tempCurr)))
                    voltList.append(voltage)
                    voltage += stepV
                self.powerOff()
                return voltList, currList
                    

        
    
class DSOX1102G(pyvisaResource):
    def __init__(self):
        # VISA CONNECTIONS
        pyvisaResource.__init__(self)
        self.connectDevice("DSO-X 1102G") # Opens oscilloscope as a pyvisa resource saved to self.instr
        self.isRunning = False
       


    def resetFactory(self):
        """Reset to factory settings"""
        self.instr.write("*RST")

    def runStop(self):
        if self.isRunning == False:
            self.instr.write(":RUN")
            self.isRunning = True
        elif self.isRunning == True:
            self.instr.write(":STOP")
            self.isRunning = False
    def singleRun(self):
        self.instr.write(":SINGLE")
        while True:
            sleep(0.2)
            self.instr.write("*OPC?")
            if self.instr.read().strip() == "1":
                break

    def displayOff(self, channel: int):
        self.instr.write(":CHANnel" + str(channel) + ":DISPlay 0")

    def displayOn(self, channel: int):
        self.instr.write(":CHANnel" + str(channel) + ":DISPlay 1")

    def setDisplay(self, channel: int, voltageRange_V: float, timeRange_s: float):
        """Sets voltage and time ranges for chosen channel and turns it on. 
          Voltage division = voltageRange / 8. Time division = timeRange/10.
          VoltageRange allowed values [40mV - 800V]. Turns the channel on."""
        self.instr.write(":CHANnel" + str(channel) + ":RANGe " + str(voltageRange_V))
        self.instr.write(":TIMebase:RANGe " + str(timeRange_s))
        self.instr.write(":CHANnel" + str(channel) + ":DISPlay 1")

    def setChannelVolt(self, channel, voltageRange_V):
        self.instr.write(":CHANnel" + str(channel) + ":RANGe " + str(voltageRange_V))
    
    def setTriggerChannel(self, channel):
        self.instr.write(":TRIGger:SOURce CHANnel" + str(channel))

    def setTriggerValue(self, triggerValue):
        self.instr.write(":TRIGger:LEVel " + str(triggerValue))
    
    def setTimeRange(self, timeDiv_s):
        """Set the time range for horizontal axis."""
        self.instr.write(":TIMebase:RANGe " + str(timeDiv_s))
    
    def setTimePosition(self, timePos_s):
        self.instr.write(":TIMebase:POSition " + str(timePos_s))

    def setWaveGen(self, amplitude, width, frequency):
        self.instr.write(":WGEN:FREQuency "+str(frequency))
        self.instr.write(":WGEN:FUNCtion PULse")
        self.instr.write(":WGEN:FUNCtion:PULSe:WIDTh "+str(width))
        self.instr.write(":WGEN:VOLTage:LOW 0")
        self.instr.write(":WGEN:VOLTage:HIGH "+str(amplitude))
        self.instr.write(":WGEN:OUTPut 0")
        
    def saveData(self, channel: int):
        """Reads binary data from oscilloscope, and formats it to voltages. 
        Returns time and voltage data as lists. Does not trigger a new measurement, simply reads what is shown in screen."""
        
        self.instr.write(f":WAVeform:SOURce CHAN{channel}") # Choose the target for waveform commands
        self.instr.write(":WAV:SOUR?")
        timeScale = float(self.instr.query(":TIMebase:RANGE?"))
        yIncrement = float(self.instr.query(":WAVeform:YINCREMENT?"))
        yOrigin = float(self.instr.query("WAVeform:YORIGIN?"))
        self.instr.write("WAV:POIN MAX") # Take maximum number of datapoints
        dataList = []
        #self.instr.write(f":DIGitize CHANnel{channel}") #The :DIGitize command is a specialized RUN command. Stops when data aqusition is complete.
        values = self.instr.query_binary_values(":WAVeform:DATA?", datatype = "B") #The :WAVeform:DATA query returns the binary block of sampled data points transmitted using the IEEE 488.2 arbitrary block data format.
        for value in values:
            # Scales binary data to volts.
            dataList.append((value-128)*yIncrement+yOrigin)
        time = np.linspace(0, timeScale, len(dataList)) #Time axis
        return time, dataList
    
    def photonCountSingle(self, peakHeight, distance, prominence, channel = 1, useOGcount = False):
        """Used for setting correct peak height, distance and prominence. Manually count peaks from oscilloscope and compare results."""
        time, voltageData = self.saveData(channel)
        return data.peakCounter(voltageData, peakHeight=peakHeight, distance=distance, prominence=prominence, useOriginal=useOGcount)
    
    def photonCount(self, numberOfDatasets, peakHeight, distance, prominence, name = "photonDistribution", channel = 1, useOGcount = False):
        """Counts pulses from screen numberOfDatasets times and returns an array with photon count of each set."""
        self.instr.write(":RUN")

        photonDistribution = np.empty(numberOfDatasets)
        i = 0
        while i < numberOfDatasets:
            voltage = self.saveData(channel = channel)[1]
            photonDistribution[i] = data.peakCounter(voltage, peakHeight=peakHeight, distance=distance, prominence=prominence, useOriginal=useOGcount)
            print(f"Measurement {i/numberOfDatasets*100} %")
            i += 1
        return photonDistribution

    def saveImage(self):
        """Saves current image shown from oscilloscope and returns PNG data"""
        self.instr.write(":HARDcopy:INKSaver OFF") #darkmode
        sDisplay = self.instr.query_binary_values(":DISPlay:DATA? PNG", datatype = "B", header_fmt = "ieee", container = bytes)
        return sDisplay
    