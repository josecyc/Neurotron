#! /usr/bin/env python3
import sys, time
import pandas as pd
import numpy as np
import src.gt_module as gt_module
import src.neuro_ml as neuro_ml
import argparse

def stream():
	pass

def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('data')
	parser.add_argument('--predict', '-p', action='store_true')
	parser.add_argument('--model', '-m')
	return parser.parse_args()

def preproc(data_set, seq_length=24):
	df = pd.read_csv(data_set)
	feature_ar = df.loc[:, 'ch1':'ch8'].values
	label_ar = df.loc[:, 'Wrist x':].values
	features, labels = neuro_ml.overlap_samples(seq_length, feature_ar, label_ar)
	return features, labels

if __name__ == '__main__':
	args = parse()
	features, labels = preproc(args.data)	
	model_file = args.model if args.model else 'model.h5'
	if args.predict:
		print('Streaming predictions to godot...')
		ml = neuro_ml.NeuroML()
		ml.load_model(model_file)
		for datum in features:
			gt_module.send_to_godot(ml.predict_sequence(datum.reshape([1, 24, 8]))[0])
	else:
		print('Streaming label data to godot...')
		for datum in labels:
			gt_module.send_to_godot(datum)
			time.sleep(0.1)
