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





""" oscillo.command(f":ACQuire:SEGMented:INDex {5}")
timeee, voltage = oscillo.saveData(channel = 1)
plt.plot(timeee, voltage)
plt.show() """


""" lotOfData = {}
for i in range(500):
    oscillo.singleRun()
    timeee, dataa = oscillo.saveData(1)
    timeee = list(timeee)
    lotOfData[i] = timeee, dataa
data.writeDictJson(lotOfData)
 """


# After pulsing
""" afterPulse25V = {1.0: 2190, 2.0: 286, 3.0: 23, 4.0: 1}
afterPulse25_5V = {1.0: 2059, 2.0: 391, 3.0: 43, 4.0: 6, 5.0: 1}
afterPulse26V = {1.0: 1878, 2.0: 507, 3.0: 93, 4.0: 17, 5.0: 4, 7.0: 1}

afterPulse25Vdarkk = {1.0: 403, 2.0: 83, 3.0: 12, 4.0: 2}
afterPulse26Vdarkkk = {1.0: 362, 2.0: 106, 3.0: 24, 4.0: 5, 5.0: 3}



print(data.afterPulseProb(afterPulse25V))
print(data.afterPulseProb(afterPulse25_5V))
print(data.afterPulseProb(afterPulse26V))
print(data.afterPulseProb(afterPulse25Vdarkk))
print(data.afterPulseProb(afterPulse26Vdarkkk))

 """

#print(data.createPhotonsDictAfterPulseCompensated())



""" #oscillo.singleRun()

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
#meanLED = data.createPhotonsDict()
#data.writeDictJson(meanLED)
#print(meanLED)

darkCount = {"27": 0.594, "27.5":0.6428,  "28": 0.6916, "28.5":0.7632, "29": 0.8348, "29.5": 0.9299, "30": 1.0252}
UVphotons = {"27": 5.3936, "27.5": 5.624, "28": 5.8636, "28.5": 6.0242, "29": 6.3216, "29.5": 6.5682, "30": 6.711}

UVdarkCountComp = {}
for key in darkCount:
    UVdarkCountComp[key] = UVphotons[key] - darkCount[key]

print(UVdarkCountComp)


""" photons = {"22.9": 0.8972, "23.4": 1.1428, "23.9": 1.41, "24.4": 1.6696, "24.9": 2.1584, "25.4": 3.1656, "25.9": 4.9528}
ap = {"22.9": 1.191, "23.4": 1.195, "23.9": 1.237, "24.4": 1.377, "24.9": 1.553, "25.4": 1.714, "25.9": 2.105}
photonsCompens = {}


for key in photons:
    photonsCompens[key] = photons[key] / (ap[key])
print(photonsCompens)
 """

""" 
afterPulses = {"24": 1.336, "24.2": 1.584, "24.4": 1.576, "24.599999999999998": 1.7, "24.799999999999997": 1.852, "24.999999999999996": 2.12, "25.199999999999996": 2.388, "25.399999999999995": 2.68, "25.599999999999994": 3.112, "25.799999999999994": 3.864, "25.999999999999993": 4.864}
photons = [value - 1 for value in list(afterPulses.values())]
bias = [float(value) for value in list(afterPulses.keys())]
plt.scatter(bias, photons, c = "purple", label = "9 K, afterpulses")
plt.xlabel("Bias voltage / V")
plt.ylabel("Afterpulses per dark count")
#plt.xticks((24, 24.5, 25, 25.5, 26), ("24", "24.5", "25", "25.5", "26"))
plt.legend()
plt.show() """





""" photoDict = data.readDictJson()
print(photoDict)

relPDEdict, refKey = data.relativePDEdict(photoDict)
print(relPDEdict)
print(refKey)

 """

# save image protocol

""" oscillo = DSOX1102G() 
testImage = oscillo.saveImage()
path = data.ChooseFolder()
data.saveOscilloImage(path, "1KfoutNoise", testImage)
 """


