from Devices import Keithley6487, pyvisaResource, DSOX1102G
import time
import pyvisa as visa
import dataHandling as data
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import *

""" rm = visa.ResourceManager()
resut = rm.list_resources()
print(resut)

sour = rm.open_resource(resut[2])
print(sour)
sour.write("*IDN?")
print(sour.read())
sour.close() """


""" testK = Keithley6487()
print(testK.get_voltRange())
testK.command("RST*")


time.sleep(1)
testK.set_voltage(1)
print(testK.get_voltage())
testK.set_currLimit(3E-3)
print(testK.get_currLimit())
testK.set_currRange(1E-3)
volt, curr = testK.IVsweep(1, 3, 0.5, 10)
for V, I in zip(volt, curr):
    print(f"Voltage1 {V}, current1 {I}")
testK.closeResource() """


""" oscillo = DSOX1102G()


#oscillo.singleRun()

timeAx1, volt1 = oscillo.saveData(1)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(timeAx1, volt1, color = "yellow")

timeax2, volt2 = oscillo.saveData(2)
ax2.plot(timeax2, volt2, color = "green")

plt.show() """

""" photoDist = oscillo.photonCount(5, 12e-3, 10, 7e-3)
print(photoDist)

data.plotPhotonDistribution(photoDist)

data.photoDistToCSV("test", photoDist)
photoDistNew = np.genfromtxt("./dataCollection/14082024test1.csv", delimiter=",")
print(photoDistNew)
data.plotPhotonDistribution(photoDistNew) """


# Distributions to a plot -protocol

# Read files and save photonLambda[volt] = lambda dictionary to a json file
meanLED = data.createPhotonsDict()
data.writeDictJson(meanLED)
print(meanLED)

#meanDark = data.createPhotonsDict()
#data.writeDictJson(meanDark)

#meanLED = data.readDictJson()


#data.writeDictJson(meanLED)


""" photoDict = data.readDictJson()
print(photoDict)

relPDEdict, refKey = data.relativePDEdict(photoDict)
print(relPDEdict)
print(refKey)

 """

# save image protocol 
""" testImage = oscillo.saveImage()
path = data.ChooseFolder()
data.saveOscilloImage(path, "photonPulseBlueLED27V", testImage) """



