#! /usr/bin/env python3
import sys, time
import pandas as pd
import numpy as np
import gt_module
import neuro_ml

def stream():
	pass

def preproc(data_set, seq_length=24):
	df = pd.read_csv(data_set)
	feature_ar = df.loc[:, 'ch1':'ch8'].values
	label_ar = df.loc[:, 'Wrist x':].values
	features, labels = neuro_ml.overlap_samples(seq_length, feature_ar, label_ar)
	return features, labels

if __name__ == '__main__':
	predict = False
	if len(sys.argv) != 2:
		print('usage: ./rfd data_set')
		exit()
	features, labels = preproc(sys.argv[1])	
	if predict:
		ml = neuro_ml.NeuroML()
		ml.load_model('model.h5')
		for datum in features:
			gt_module.send_to_godot(ml.predict_sequence(datum.reshape([1, 24, 8]))[0])
	else:
		for datum in labels:
			gt_module.send_to_godot(datum)
			time.sleep(0.1)
