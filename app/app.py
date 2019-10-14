#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  app.py                                                                      #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday October 2019 7:12:26 pm                                     #
#  Modified: Sunday Oct 2019 7:32:01 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

from myo_core import MyoBT

def handler(myo, emg):
	for i, data in enumerate(emg):
		print(f'ch{i}: {data}', end=' ')
	print('')

if __name__ == "__main__":
	myo = MyoBT()
	myo.assign_emu_handler(handler)
	myo.run()
