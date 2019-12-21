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
	parser.add_argument('--angles', '-a', action='store_true')
	parser.add_argument('--seq', '-s', type=int)
	parser.add_argument('--model', '-m')
	parser.add_argument('--compare', '-c', action='store_true')
	return parser.parse_args()

def preproc(data_set, seq_length=240):
	df = pd.read_csv(data_set)
	feature_ar = df.loc[:, 'ch1':'ch8'].values
	label_ar = df.loc[:, 'Wrist x':].values
	features, labels = neuro_ml.overlap_samples(seq_length, feature_ar, label_ar)
	return features, labels

def coords_to_angles_row(labels):
    ls_row = []
    for j in range(3):
        for i in range(0, 12, 3):
            label_x_or = labels[i + j * 12]

            label_y_or = labels[i + 1 + j * 12]

            label_x_obj = labels[i + 3 + j * 12] - label_x_or

            label_y_obj = labels[i + 4 + j * 12] - label_y_or

            h = np.sqrt(label_x_obj**2 + label_y_obj**2)

            ls_row.append(np.degrees(np.arccos(label_y_obj/h)))

    return ls_row

if __name__ == '__main__':
	args = parse()
	features, labels = preproc(args.data, args.seq)	
	model_file = args.model if args.model else 'model.h5'
	print('\nmodel: {}\nsequence: {}\n'.format(model_file, args.seq))
	if args.predict:
		print('Streaming predictions to godot...')
		ml = neuro_ml.NeuroML()
		ml.load_model(model_file)
		for datum, label in zip(features, labels):
			if args.angles:
				gt_module.send_to_godot_angles(ml.predict_sequence(datum.reshape([1, 24, 8]))[0])
			else:
				gt_module.send_to_godot(ml.predict_sequence(datum.reshape([1, args.seq, 8]))[0])
			if args.compare:
				gt_module.send_to_godot_compare(label)
				time.sleep(0.1)
	else:
		print('Streaming label data to godot...')
		for datum in labels:
			gt_module.send_to_godot(datum)
			time.sleep(0.1)
