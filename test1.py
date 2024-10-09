from Devices import Keithley6487, pyvisaResource, DSOX1102G
import time
import pyvisa as visa
import dataHandling as data
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import *
from collections import Counter

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


""" oscillo = DSOX1102G()
lotOfData = {}
for i in range(50):
    oscillo.singleRun()
    timeee, dataa = oscillo.saveData(1)
    timeee = list(timeee)
    lotOfData[i] = timeee, dataa
data.writeDictJson(lotOfData) """



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

""" 
oscillo = DSOX1102G()

apTrainDict = {}

segIndex = 1
while segIndex <= 50:
    oscillo.command(f":ACQuire:SEGMented:INDex {segIndex}")
    time.sleep(0.1)
    timeDat, voltage = oscillo.saveData(channel = 1)
    timeDat = [dat - 50e-6 for dat in timeDat]
    apTrainDict[segIndex] = (timeDat, voltage)
    plt.plot(timeDat, voltage, color = "orange")
    
    segIndex += 1

plt.show()
data.writeDictJson(apTrainDict) """

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
#data.writeDictJson(meanLED)
print(meanLED)




""" dark = {'53.3': 0.536, '53.8': 0.654, '54.3': 0.766, '54.8': 0.89, '55.3': 1.027, '55.8': 1.074, '56.3': 1.255, '56.8':1.268}
base = {"53.3": 3.2468, "53.8": 3.6668, "54.3": 3.8444, "54.8": 3.91, "55.3": 4.2448, "55.8": 4.492, "56.3": 4.694, "56.8": 4.9292}

legit = [key1 - key2 for key1, key2 in zip(base.values(), dark.values())]
print(legit) """





""" photons = {"22.9" : 0.2248, "23.4": 0.3088, "23.9": 0.3776, "24.4": 0.4808, "24.9": 0.6612, "25.4": 0.8748, "25.9": 1.442}
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




# Save pulse shapes
""" oscillo = DSOX1102G()
timeee, volt = oscillo.saveData(1)
tempDick = {}
for t, v in zip(timeee, volt):
    tempDick[t] = v
data.writeDictJson(tempDick, initdir="C:/Users/hydrogen/Documents/Tom_Sampsa/SiPMs/SiPMs/dataCollection/HAMAMATSU") """



# Plot pulse shapes
""" doct  = data.readDictJson("C:/Users/hydrogen/Documents/Tom_Sampsa/SiPMs/SiPMs/dataCollection/HAMAMATSU")
timeDat = [float(key) for key in doct.keys()]
voltDat = [float(val) for val in doct.values()]
plt.plot(timeDat, voltDat, color = "red")

doct2  = data.readDictJson("C:/Users/hydrogen/Documents/Tom_Sampsa/SiPMs/SiPMs/dataCollection/HAMAMATSU")
timeDat = [float(key) for key in doct2.keys()]
voltDat = [float(val) for val in doct2.values()]

plt.plot(timeDat, voltDat)
plt.show()
 """

# save image protocol
""" 
oscillo = DSOX1102G() 
testImage = oscillo.saveImage()
path = data.ChooseFolder()
data.saveOscilloImage(path, "1060Ohm1_9VoverVoltBadPDEtunnelingExplodes", testImage) """


