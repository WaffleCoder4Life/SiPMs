from Devices import Keithley6487,DSOX1102G
import dataHandling as data
from time import sleep


waveGenSet = (2.4,300e-9,500)
oscilloSet = (1, 32e-3, 100e-6)
photoSettings = (250, 0.001, 10, 0.003, "photonDistribution", 1, False, True)


def afterPulseSweep1(oscillo, power, startVolt, endVolt, waveGenSettings:list, oscilloSettings:list,  extraFunctio1, peakCountSettings:list,):
    oscillo = oscillo
    powerSource = power

    # SETUP MEASUREMENT
    oscillo.setWaveGen(*waveGenSettings)
    oscillo.setDisplay(*oscilloSettings)
    oscillo.setTriggerChannel(1)
    oscillo.setTriggerValue(3e-3)
    oscillo.command(":TIMebase:POSition " + str(48e-6))

    _, _, photoCount = powerSource.IVsweep(startV=startVolt, endV=endVolt, stepV=0.2, extraFunctio=extraFunctio1, args=peakCountSettings)
    voltLambdaDict = {}
    for tuple in photoCount:
        voltLambdaDict[tuple[0]] = data.plotPhotonDistribution(tuple[1], plotShow=False)

    print(voltLambdaDict)
    data.writeDictJson(voltLambdaDict)


def afterPulseCounting(oscillo, pulseHeight, pulseDist, pulsePromi, pulseMax, name):
    #tim, volt = oscillo.saveData(1)
    #print(len(volt))
    dist = oscillo.afterPulseProb(1000, pulseHeight, pulseDist, pulsePromi, pulseMax)
    data.photoDistToCSV(name, dist, f"New protocol; 5 us prior to trigger must be empty, triggered on 1 P.E. dark counts, counting pulses from 5 us window.\n pulse height {pulseHeight}, pulse distance {pulseDist}, pulse prominence {pulsePromi} and max pulse {pulseMax}")
    data.plotPhotonDistribution(dist)



def main():
    oscillo = DSOX1102G()
    sleep(1)
    power = Keithley6487()
    sleep(1)
    afterPulseSweep1(oscillo = oscillo, power = power, startVolt= 23, endVolt=26, waveGenSettings= waveGenSet, oscilloSettings= oscilloSet, extraFunctio1 = oscillo.photonCount, peakCountSettings=photoSettings)
    #afterPulseCounting(oscillo, 0.001, 10, 0.001, 0.004, "Dale1KafterPulseDist22_9V")

if __name__ == "__main__":
    main()