# File for testing different peak finding algorithms

import dataHandling as data
import matplotlib.pyplot as plt




# 500 pulses recorded at 60 K to be used as testing data

def jsonToLists():
    dataDictionary = data.readDictJson(filePath="C:/Users/hydrogen/Documents/Tom_Sampsa/SiPMs/SiPMs/peakFilterTestingData24_5VPt60.json")
    timeDataList = []
    voltDataList = []
    for key in dataDictionary:
        timeDataList.append(dataDictionary[key][0])
        voltDataList.append(dataDictionary[key][1])
    return timeDataList, voltDataList


def peakFinder1():
    timeDataList, voltDataList = jsonToLists()
    for i in range(5):
        plotPulse(timeDataList[i], voltDataList[i])
        plt.show()


def plotPulse(timeData, voltData):
    plt.plot(timeData, voltData)
    plt.show()

def main():
    peakFinder1()




if __name__ == "__main__":
    main()