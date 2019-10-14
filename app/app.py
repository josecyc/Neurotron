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
from neuro_ml import NeuroML
import os

def handler(myo, emg):
	for i, data in enumerate(emg):
		print(f'ch{i}: {data}', end=' ')
	print('')

def ml_handler(myo, emg):
	predict = ml.predict(emg)
	os.system('cls' if os.name == 'nt' else 'clear')
	print('q len:', len(ml.q))
	print(predict)

if __name__ == "__main__":
	ml = NeuroML()
	ml.load_model('model.h5')
	myo = MyoBT()
	myo.assign_emg_handler(ml_handler)
	myo.run()
