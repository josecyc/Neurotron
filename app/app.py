#! /usr/bin/env python3
# ---------------------------------------------------------------------------- #
#  app.py                                                                      #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday October 2019 7:12:26 pm                                     #
#  Modified: Sunday Oct 2019 7:32:01 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

from src.myo_core import MyoBT
from src.neuro_ml import NeuroML
import os, time
import numpy as np
from collections import deque
import src.gt_module as gt_module
import argparse
import multiprocessing

def handler(myo, emg):
	for i, data in enumerate(emg):
		print(f'ch{i}: {data}', end=' ')
	print('')

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('--model', '-m')
	parser.add_argument('--seq', '-s', help='model sequence length', type=int, default=32)
	return parser.parse_args()

q_loc = deque()

def producer_handler(myo, emg):
	q_loc.append(np.array(emg, dtype='float64'))
	if len(q_loc) > seq_len:
		q_loc.popleft()
	print('q len:', q.qsize())
	if q.qsize() < 2 and len(q_loc) == seq_len:
		q.put(np.array(q_loc).reshape([1, seq_len, 8]))

def producer(q):
	myo = MyoBT()
	myo.assign_emg_handler(producer_handler)
	myo.run()

def consumer(q, model_file):
	ml = NeuroML()
	ml.load_model(model_file)
	while True:
		now = time.time()
		data = q.get()
		predict = ml.predict_sequence(data)
		gt_module.send_to_godot(predict[0])
		fr = 1 / (time.time() - now)
		print('framerate:', fr)

if __name__ == "__main__":
	args = parse()
	global seq_len
	seq_len = args.seq
	model_file = args.model if args.model else '../models/FC_arch_jackson_all_joints_model.h5'
	q = multiprocessing.Queue()

	producer = multiprocessing.Process(target=producer, args=(q,))
	producer.daemon = True

	consumer = multiprocessing.Process(target=consumer, args=(q,model_file))
	consumer.daemon = True

	print('Starting sub processes...')
	consumer.start()
	producer.start()

	while True:
		pass
