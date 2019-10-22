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
import os, time
import numpy as np
from collections import deque
import gt_module
import argparse

def handler(myo, emg):
	for i, data in enumerate(emg):
		print(f'ch{i}: {data}', end=' ')
	print('')

def ml_handler(myo, emg):
	start = time.time()
	predict = ml.predict(emg)
	end = time.time()

	os.system('cls' if os.name == 'nt' else 'clear')
	print('predict time: {}'.format(start - end))
	print('q len:', len(ml.q))
	if predict is not None:
		print(predict.shape)
		gt_module.send_to_godot(predict)
	print(predict)

def ml_sequence_handler(myo, emg):
	q.append(np.array(emg, dtype='float64'))
	print('q len:', len(q))
	if len(q) == 24:
		predict = ml.predict_sequence(np.array(q).reshape([1, 24, 8]))
		print(predict)
		gt_module.send_to_godot(predict[0])
		q.clear()

count = 0
start_t = time.time()

def latency_test_handler(myo, emg):
	global start_t
	period_t = 1
	q.append(np.array(emg, dtype='float64'))
	global count
	count += 1
	now = time.time()
	if now - start_t > period_t:
		start_t = now
		print('packets this period:', count)
		count = 0
		q.clear()
	
def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('--model', '-m')
	return parser.parse_args()

if __name__ == "__main__":
	args = parse()
	model_file = args.model if args.model else 'model.h5'
	q = deque()
	ml = NeuroML()
	ml.load_model(model_file)
	myo = MyoBT()
	myo.assign_emg_handler(ml_handler)
	myo.run()
