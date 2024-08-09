from Devices import Keithley6487, pyvisaResource, DSOX1102G
import time
import pyvisa as visa
import dataHandling as data


testK = Keithley6487()
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
testK.closeResource()


""" oscillo = DSOX1102G()
oscillo.setDisplay(1, 800, 10)
oscillo.setDisplay(2, 40E-3, 1000E-6)
oscillo.displayOff(2)
oscillo.command(":SINGLE") """
#timeAx1, volt1 = oscillo.saveData(1)
# tST COMMITIT

"""
# save image protocol 
testImage = oscillo.saveImage()
path = data.ChooseFolder()
data.saveOscilloImage(path, "testImage", testImage) """



