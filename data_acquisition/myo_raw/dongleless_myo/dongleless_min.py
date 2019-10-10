from __future__ import print_function
from bluepy import btle
import myo_dicts
import struct
import socket
import json
import time
import math
import pprint
import logging as log
import subprocess
import sys
import os
import csv

PATH = os.getcwd()

busylog = False #decides whether emg/imu notifications will generate log messages.
log.basicConfig(filename=PATH+"/dongleless.log", filemode = 'w', level = log.CRITICAL, #change log.CRITICAL to log.DEBUG to get log messages
				format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%H:%M:%S')

def write_to_csv(emg):
    with open('emg_data_002_jose.csv', 'a') as fd:
        writer = csv.writer(fd)
        emg = list(emg)
        emg.insert(0, time.time())
        #print('emg', emg)
        writer.writerow(emg)

class Connection(btle.Peripheral):
	def __init__(self, mac):
		btle.Peripheral.__init__(self, mac)

		# self.writeCharacteristic(0x19, struct.pack('<bbbbb', 0,0,0,3,1) ,True ) # Tell the myo we want neither IMU nor classifier data
		# self.writeCharacteristic(0x24, struct.pack('<bb', 0x00, 0x00),True) # Unsubscribe from classifier indications

		# time.sleep(0.5)

		self.writeCharacteristic(0x24, struct.pack('<bb', 0x02, 0x00),True) # Subscribe to classifier indications
		self.writeCharacteristic(0x1d, struct.pack('<bb', 0x01, 0x00),True) # Subscribe to imu notifications
		self.writeCharacteristic(0x28, struct.pack('<bb', 0x01, 0x00),True) # Subscribe to emg notifications
		self.writeCharacteristic(0x19, struct.pack('<bbbbb', 1,1,1,3,1) ,True ) # Tell the myo we want all the data

	def vibrate(self, length):
		self.writeCharacteristic(0x19, struct.pack('<bbb', 0x03, 0x01, length),True)
