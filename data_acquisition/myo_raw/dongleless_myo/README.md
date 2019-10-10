#Dongleless Myo
=======================

For if you don't have your dongle but just need to control a linux system anyway, with a different dongle or you computer's built in bluetooth.



##Setup
-------
First, get a linux system, it's mainly been tested on debian and ubuntu.

Second, go through the setup for bluez and [bluepy](https://github.com/IanHarvey/bluepy), and run the bluepy test program to make sure it works. (This step can be a bit of a pain). Make sure the bluepy files are somewhere python can see.

Download dongleless.py and put it somewhere convenient to import where it can import bluepy, and put myo_dicts.py in the same folder.

##Limitations
-------------

* Currently does not work with multiple myos. It appears bluepy can only listen to one connection at a time, and switching back and forth quickly seems to cause both myos to glitch.

* There is a glitch where sometimes the myo stops receiving classifier indications, almost always after being taken off while the program is running. Plugging the myo in or letting it go to sleep by placing it on a flat surface for ~30 seconds fixes it.

* Currently has a list of handles to read/write from, rather than using the uuids. It's possible, though unlikely, that a future firmware update will change those handles, in which case they would need to be updated in the code.

* Can't provide emg and pose data at the same time. Currently, it provides emg until it's synced, then provides poses instead.

##Usage
-------

To use, simply import dongleless.py from your project directory or somewhere on your path, and call dongleless.run with a dictionary from event names to functions which should be called to respond to them. A sample is included. Any event not in the dictionary will simply do nothing.

The myo argument to the functions represents the myo, but currently the only function it has is vibrate() which takes an int argument from 0-3 representing the vibration length.
