

import dataHandling as data
import matplotlib.pyplot as plt


def operatingReginPlot():
    # Measured while cooling down, some inaccuracities on temperature as well as definition of tunneling bd
    temperature = [295, 173, 164, 128, 94, 77.7, 61, 57, 54, 52, 49, 46, 44, 40, 37, 16.3, 12.2, 4.2]
    bdVolt = [51.3, 45, 44.6, 43.3, 42.2, 41.8, 41.58, 41.54, 41.53, 41.49, 41.49, 41.48, 41.47, 41.5, 41.5, 41.5, 41.45, 41.47]

    tempTune = [40, 37, 28, 26, 23, 18.3, 16.3, 12.2, 9, 4.2]
    tunnelVolt = [42.2, 42.1, 41.8, 41.8, 41.8, 43, 43.3, 43.4, 43.5, 43.8]


    plt.scatter(temperature, bdVolt, marker = "x", color = "blue", label = "Breakdown voltages from IV-curves")
    #plt.fill_between(temperature, bdVolt, 41, alpha = 0.5, color = "blue", hatch = '/')

    #plt.scatter(tempTune, tunnelVolt, marker = "x", color = "orange", label = "V$_{\mathrm{tunneling}}$")
    #plt.fill_between(tempTune, tunnelVolt, 44, alpha = 0.5, color = "orange", hatch = '/')


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

    hamaTemperatures = [295, 94, 77.7, 4, 1, 0.08]
    hamaBluePDE = [0.29, 0.254, 0.234, 0.185, 0.179, 0.160]

    refTemp = [295, 295]
    refPDE = [0.31, 0.29]

    onsemiUV = [0.08]

    plt.scatter(onsemiTemperatures, onsemiBluePDE, marker = "x", color = "blue", label = "Onsemi PDE$_{\mathrm{blue}}$")
    plt.scatter(hamaTemperatures, hamaBluePDE, marker = "x", color = "orange", label = "Hamamatsu PDE$_{\mathrm{blue}}$")
    plt.scatter(refTemp, refPDE, facecolor = "none", edgecolor = "black", linestyle = "--", s = 80, label = "RT reference point")

    plt.xlabel("Temperature / K")
    plt.ylabel("PDE")

    plt.legend()
    plt.show()

def PDEvsTempPlotUV():
    # PDE plots for 2.5 V overvoltage

    onsemiTemperatures = [295, 1]
    onsemiUVPDE = [0.08, 0.0051]

    hamaTemperatures = [295, 94, 77.7, 4, 1, 0.08]
    hamaUVPDE = [0.17, 0.10, 0.082, 0.00167, 0.00131, 0.000632]

    refTemp = [295, 295]
    refPDE = [0.08, 0.17]

    onsemiUV = [0.08]

    plt.scatter(onsemiTemperatures, onsemiUVPDE, marker = "x", color = "blue", label = "Onsemi PDE$_{\mathrm{UV}}$")
    plt.scatter(hamaTemperatures, hamaUVPDE, marker = "x", color = "orange", label = "Hamamatsu PDE$_{\mathrm{UV}}$")
    plt.scatter(refTemp, refPDE, facecolor = "none", edgecolor = "black", linestyle = "--", s = 80, label = "RT reference point")

    plt.xlabel("Temperature / K")
    plt.ylabel("PDE")

    plt.legend()
    plt.show()
    






def main():
    operatingReginPlot()
    #PDEvsTempPlotBlue()

if __name__ == "__main__":
    main()