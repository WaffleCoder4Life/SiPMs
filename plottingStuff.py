

import dataHandling as data
import matplotlib.pyplot as plt
from collections import Counter

def operatingReginPlot():
    # Measured while cooling down, some inaccuracities on temperature as well as definition of tunneling bd
    temperature = [295, 173, 164, 128, 94, 77.7, 61, 57, 54, 52, 49, 46, 44, 40, 37, 16.3, 12.2, 4.2]
    bdVolt = [51.3, 45, 44.6, 43.3, 42.2, 41.8, 41.58, 41.54, 41.53, 41.49, 41.49, 41.48, 41.47, 41.5, 41.5, 41.5, 41.45, 41.47]

    temperature = [ 40, 37, 16.3, 12.2, 4.2, 0.08]
    bdVolt = [41.5, 41.5, 41.5, 41.45, 41.47, 41.5]

    tempTune = [40, 37, 28, 26, 23, 18.3, 16.3, 12.2, 9, 4.2, 0.08]
    tunnelVolt = [42.2, 42.1, 41.8, 41.8, 41.8, 43, 43.3, 43.4, 43.5, 43.8, 44.5]


    plt.scatter(temperature, bdVolt, marker = "x", color = "blue", label = "Breakdown voltage")
    plt.fill_between(temperature, bdVolt, 41, alpha = 0.5, color = "blue", hatch = '/')

    plt.scatter(tempTune, tunnelVolt, marker = "x", color = "orange", label = "Tunneling breakdown")
    plt.fill_between(tempTune, tunnelVolt, 44.5, alpha = 0.5, color = "orange", hatch = '/')


    plt.xlabel("Temperature / K")
    plt.ylabel("Breakdown voltage / V")
    plt.legend()

    plt.show()


def darkCountPlot():
    voltage = [43.5, 43.7, 43.9, 44, 44.1, 44.2]
    darkCount = [0, 0, 0, 0, 0.05, 13.61]


def PDEvsTempPlotBlue():
    # PDE plots for 2.5 V overvoltage

    onsemiTemperatures = [295, 272, 165, 121, 1]
    onsemiBluePDE = [0.31, 0.294, 0.273, 0.262, 0.062]

    hamaTemperatures = [295, 94, 77.7, 4, 1, 0.390, 0.195, 0.08]
    hamaBluePDE = [0.29, 0.254, 0.234, 0.185, 0.179, 0.175, 0.163, 0.160]

    # Photocurrent comparison for 1.5 V overvoltages
    hamaBluePDEphotoCurrent = [0.29, 0.284, 0.252, 0.223, 0.186]

    refTemp = [295, 295]
    refPDE = [0.31, 0.29]

    onsemiUV = [0.08]

    plt.scatter(onsemiTemperatures, onsemiBluePDE, marker = "x", color = "blue", label = r"Onsemi PDE$_{\mathrm{blue}}$")
    plt.scatter(hamaTemperatures, hamaBluePDE, marker = "x", color = "orange", label = r"Hamamatsu PDE$_{\mathrm{blue}}$")
    plt.scatter(refTemp, refPDE, facecolor = "none", edgecolor = "black", linestyle = "--", s = 80, label = "RT reference point")

    plt.xlabel("Temperature / K")
    plt.ylabel("PDE")

    plt.legend()
    plt.show()

def PDEvsTempPlotUV():
    # PDE plots for 2.5 V overvoltage

    onsemiTemperatures = [295, 1]
    onsemiUVPDE = [0.08, 0.0051]

    hamaTemperatures = [295, 94, 77.7, 4, 1, 0.390, 0.195, 0.08]
    hamaUVPDE = [0.17, 0.10, 0.082, 0.00167, 0.00131, 0.00106, 0.000971, 0.000632]

    refTemp = [295, 295]
    refPDE = [0.08, 0.17]

    onsemiUV = [0.08]

    plt.scatter(onsemiTemperatures, onsemiUVPDE, marker = "x", color = "blue", label = r"Onsemi PDE$_{\mathrm{UV}}$")
    plt.scatter(hamaTemperatures, hamaUVPDE, marker = "x", color = "orange", label = r"Hamamatsu PDE$_{\mathrm{UV}}$")
    plt.scatter(refTemp, refPDE, facecolor = "none", edgecolor = "black", linestyle = "--", s = 80, label = "RT reference point")

    plt.xlabel("Temperature / K")
    plt.ylabel("PDE")

    plt.legend()
    plt.show()
    

def afterPulseTimeDistPlot():
    #apLoca = data.CSVtoPhotoDist("C:/Users/hydrogen/Documents/Tom_Sampsa/SiPMs/SiPMs/dataCollection/111020245400OhmAPlocations25us44V1.csv")
    apLoca = data.CSVtoPhotoDist("C:/Users/hydrogen/Documents/Tom_Sampsa/SiPMs/SiPMs/dataCollection/111020245400OhmAPlocations30us44V2.csv")
    apNew = []
    for ap in apLoca:
        ap = (ap-60000) * 0.0005 # Change to us scale
        ap = myround(ap, base = 0.5)
        apNew.append(ap)
    counts = Counter(apNew)
    sortedCounts = dict(sorted(counts.items()))
    timePos = []
    value = []
    for count in sortedCounts:
        timePos.append(count)
        value.append(sortedCounts[count])
    mediaani = median(value, 0.5)
    mediaaniYsikyt = median(value, 0.9)

    plt.scatter(timePos, value, color = "darkorange", label = "Afterpulses")
    plt.axvline(timePos[mediaani], linestyle='--', label = "50 %", color = "black")
    plt.axvline(timePos[mediaaniYsikyt], linestyle='--', label = "90 %", color = "black")
    plt.xlabel(r"Time / $\mu$s")
    plt.ylabel("Number of afterpulses")
    plt.legend()
    plt.show()

def myround(x, base=5):
    return base * round(x/base)

def median(dataList, fraction):
    totalVal = sum(dataList)
    summed = 0
    for i in range(len(dataList)):
        if summed < (fraction * totalVal):
            summed += dataList[i]
        else:
            return i


def afterPulseProbVsTimePlot():
    timeWindow = [380e-9, 5e-6, 10e-6, 15e-6]
    apProb = [0.03, 0.243, 0.362, 0.411]

    plt.plot(timeWindow, apProb)
    plt.show()


def heatFlowPlot():
    # for 0 bias/curr temperature = 0.09
    biasVoltage = [43, 43.2, 43.5, 43.7, 44]
    photoCurrent = [1.2e-8, 1.95e-8, 4e-8, 7e-8, 2.35e-7]
    temperature = [0.094, 0.103, 0.113, 0.13, 0.197]

    heatPower = [bias * curr for bias, curr in zip(biasVoltage, photoCurrent)]
    
    plt.scatter(heatPower, temperature, color = "red", label = "T(V*I)")
    plt.legend()
    plt.show()



def main():
    #operatingReginPlot()
    #PDEvsTempPlotBlue()
    PDEvsTempPlotUV()
    #afterPulseTimeDistPlot()
    #afterPulseProbVsTimePlot()
    #heatFlowPlot()

if __name__ == "__main__":
    main()