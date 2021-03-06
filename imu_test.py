# ######################################################################################################################
# ## imu_test.py
# ## Description: testing the IMU
# ##                - We test the connection and print the pitch angle.
# ## Library needed: imu, time, math, serial, sys libraries
# ## Python interpreter: Anaconda 2.2.0 (python 2.7)
# ## Author: Ana Carolina Cardoso de Sousa
# ## Email: anacsousa1@gmail.com
# ## Created: May 29th 2015
# ######################################################################################################################

__authors__ = [
    "\"Ana de Sousa\" <anacsousa1@gmail.com>",
]

# Importing...
import time
import math
import serial
import imu
import sys

# Greetings
print "Welcome to ours IMU tester, let\'s get this started?\n"

# Ports and addresses
portIMU = 'COM9'        # in windows, verify "Manage Devices"
addressIMU = 1          # the device must have a stick informing it

# Open ports
print '\tWe are trying to connect to the IMU (address ' + str(addressIMU) + ') to port ' + portIMU + '.'

try:
    serialPortIMU = serial.Serial(portIMU, timeout=1, writeTimeout=1, baudrate=115200)
except serial.SerialException:
    print '\t\tNo Hardware Found in ' + portIMU + '... :(\n \t\tExiting now. \n'
    sys.exit(0)

if not serialPortIMU.isOpen():  # verify if it is already open
    serialPortIMU.open()

device1 = imu.IMU(serialPortIMU, addressIMU)    # Construct object

testing = device1.getEulerAngles()              # Get some info
testing = testing.split(',', 6)                 # Convert to list

if len(testing) == 2:   # testing connection
    print '\t\tUnable to connect to the IMU... :(\n \t\tExiting now. \n'
    sys.exit(1)

# Calibrating
print '\t\tWe are connected! Now, we are going to calibrate the IMU. Keep it still!\n'

device1.calibrate()
device1.tare()

print "\t\t\tIMU Calibrated!\n"

# Wait until the user press the 'Start' button
print '\n\t\tWhenever you\'re ready, press button 1 (the left one)!'
while not (device1.checkButtons() == 1):
    pass

# Do it while 'Stop' button not pressed
dt = 0.5
print '\nPrinting pitch angle (sample time ' + str(dt) + ' seconds).'

while not (device1.checkButtons() == 2):
    angles = device1.getEulerAngles()   # get angles
    angles = angles.split(',', 6)       # convert to list

    if len(angles) == 6:                # if we connect correctly with the device
        pitch = float(angles[4])
        if pitch >= 0:
            pitch = math.degrees(pitch)
        else:
            pitch = 360 + math.degrees(pitch)
        print str(pitch)

    time.sleep(dt)

# Bye bye
serialPortIMU.close()                   # close port
print 'Have a nice day!'
