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
        # writeCharacteristic(handle, val, withResponse=False): writes the data val to the characteristic identified by handle
        # This is useful if we know the charasteristic's GATT handle, but do not have a characteristic object

		# self.writeCharacteristic(0x19, struct.pack('<bbbbb', 0,0,0,3,1) ,True ) # Tell the myo we want neither IMU nor classifier data
		# self.writeCharacteristic(0x24, struct.pack('<bb', 0x00, 0x00),True) # Unsubscribe from classifier indications

		self.writeCharacteristic(0x24, struct.pack('<bb', 0x02, 0x00),True) # Subscribe to classifier indications
		self.writeCharacteristic(0x1d, struct.pack('<bb', 0x01, 0x00),True) # Subscribe to imu notifications
		self.writeCharacteristic(0x28, struct.pack('<bb', 0x01, 0x00),True) # Subscribe to emg notifications
		self.writeCharacteristic(0x19, struct.pack('<bbbbb', 1,1,1,3,1) ,True ) # Tell the myo we want all the data

	def vibrate(self, length):
		self.writeCharacteristic(0x19, struct.pack('<bbb', 0x03, 0x01, length),True)

class MyoDelegate(btle.DefaultDelegate):
	def __init__(self, bindings, myo):
		self.bindings = bindings #bindings is function dict
		self.myo = myo

	def handleNotification(self, cHandle, data):
		if cHandle == 0x1c: # IMU
			data = struct.unpack('<10h', data)
			quat = data[:4]
			accel = data[4:7]
			gyro = data[7:]
			if busylog:
				log.debug("got imu notification")
			ev_type = "imu_data"
			if "imu_data" in self.bindings:
				self.bindings["imu_data"](self.myo, quat, accel, gyro)

		elif cHandle == 0x27: # EMG
			data = struct.unpack('<8HB', data) # an extra byte for some reason
			#print('data', data)
			if busylog:
				log.debug("got emg notification")
			ev_type = "emg_data"
			if "emg_data" in self.bindings:
				self.bindings["emg_data"](self.myo, data[:8])
			write_to_csv(data[:8])

def print_wrapper(*args):
	print(args)

#take a list of the events.
events = ("rest", "fist", "wave_in", "wave_out", "wave_left", "wave_right",
"fingers_spread", "double_tap", "unknown","arm_synced", "arm_unsynced",
"orientation_data", "gyroscope_data", "accelerometer_data", "imu_data", "emg_data")

# Bluepy is more suited to getting default values like heartrate and such, it's not great at fetching by uuid.

def find_myo_mac(blacklist):
	sts = subprocess.Popen("sudo timeout -s SIGINT -k 0 3 sudo hcitool lescan > "+PATH+"/scan_results.txt", shell=True).wait()
	with open(PATH+"/scan_results.txt") as res:
		lines = list(res)
	lis = []
	for line in lines:
		print('line:', line)
		sp = line.split(' ')
		if sp[-1] == 'Myo\n':
			lis.append(sp[0])
			print('found MYOO')
			return lis
	return lis

def run(modes):
# Takes one argument, a dictionary of names of events to functions to be called when they occur.
	# Main loop --------
	while True:
		blacklist = []
		try:
			log.info("Initializing bluepy connection.")
			p=None
			while not p:
				print('WTF')
				x=find_myo_mac(blacklist)
				print('x:', x)
				for mac in x:
					try:
						p = Connection( mac ) # Takes a long time if it's not a myo
						if p:
							break
					except btle.BTLEException:
						log.info("Found something that is not a Myo, adding to blacklist and trying again.")
						log.debug("could not write to %s, ignored" % mac)
						del p
						p=None
						blacklist.append(mac)
						time.sleep(0.5)
					else:
						log.info("Found Myo at MAC: %s" % mac)
			p.setDelegate( MyoDelegate(modes, p))

			log.info("Initialization complete.")
			while True:
				# break
				try:
					p.waitForNotifications(3)
				except btle.BTLEException:
					log.info("Disconnected")
					break
		except KeyboardInterrupt:
			log.warning("KeyboardInterrupt")
			break
		# except:
		#     log.critical("Unexpected error:", sys.exc_info()[0])
	log.warning("Program stopped")

def imu_data(myo, quat, accel, gyro):
    #print("imu_data:", quat)
    return

def emg_data(myo, emg, times=[]):
    print("emg_data:", emg)

function_dict = {
"imu_data":imu_data,
"emg_data":emg_data
}

run(function_dict)
if '__name__'=='__main__':
    run(function_dict)
