# ---------------------------------------------------------------------------- #
#  neuro_ml.py                                                                 #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday October 2019 7:22:07 pm                                     #
#  Modified: Friday Oct 2019 3:20:48 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

from collections import deque
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model

class Autoencoder:
	def __init__(self, input_dim=63, encoding_dim=9):
		input_vec = Input(shape=(input_dim,))
		dense_0 = Dense(32, activation=None)(input_vec)
		dense_1 = Dense(16, activation=None)(dense_0)
		encoded = Dense(encoding_dim, activation=None)(dense_1)
		dense_2 = Dense(32, activation=None, name='decoder_0')(encoded)
		dense_3 = Dense(16, activation=None, name='decoder_1')(dense_2)
		decoded = Dense(63, activation=None, name='decoder_output')(dense_3)
		self.autoencoder = Model(input_vec, decoded)
		optimizer = tf.keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
		self.autoencoder.compile(optimizer=optimizer, loss='mean_squared_error')

		# Encoder from autoencoder
		self.encoder = Model(input_vec, encoded)

		# Decoder from autoencoder layers
		decoder_input = Input(shape=(encoding_dim,), name='encoded_input')
		decode_0 = self.autoencoder.layers[-3](decoder_input)
		decode_1 = self.autoencoder.layers[-2](decode_0)
		decode_output = self.autoencoder.layers[-1](decode_1)
		self.decoder = Model(decoder_input, decode_output, name='decoder')
	def train(self, labels):
		self.autoencoder.fit(labels, labels, batch_size=512, epochs=25, verbose=1, validation_split=0.2)

class LSTM_Module:
	def __init__(self, autoencoder):
		#lstm layers
		inputs = Input(shape=(None, 8), name="inputs")
		lstm_0 = LSTM(64, return_sequences=True, name="lstm_0")(inputs)
		do = Dropout(0.2)(lstm_0)
		lstm_1 = LSTM(64, return_sequences=False, name="lstm_1")(do)
		lstm_out = Dense(9, activation=None, name="lstm_out")(lstm_1)

		#decoder layers
		decoder_0 = autoencoder.decoder.get_layer("decoder_0")(lstm_out)
		decoder_0.trainable = False
		decoder_1 = autoencoder.decoder.get_layer("decoder_1")(decoder_0)
		decoder_1.trainable = False
		decoder_output = autoencoder.decoder.get_layer("decoder_output")(decoder_1)
		decoder_output.trainable = False

		self.model = Model(inputs, decoder_output, name="model_v1")
		optimizer = tf.keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.00, amsgrad=False)
		self.model.compile(optimizer=optimizer, loss='mse')
	def train(self, features, labels, seq_length=24, epochs=4, verbose=1, validation_split=0.2):
		self.model.fit(features, labels, batch_size=seq_length, epochs=epochs, verbose=verbose, validation_split=validation_split)

class Dense_Module:
	def __init__(self, seq_length):
		self.model_fc = tf.keras.models.Sequential()
		self.model_fc.add(LSTM(256, return_sequences=True, input_shape=(seq_length, 8)))
		self.model_fc.add(Dropout(0.5))
		self.model_fc.add(LSTM(256, return_sequences=True))
		self.model_fc.add(Dropout(0.5))
		self.model_fc.add(LSTM(128))
		self.model_fc.add(BatchNormalization())
		self.model_fc.add(Dense(512, input_dim=128))
		self.model_fc.add(Activation('relu'))
		self.model_fc.add(BatchNormalization())
		self.model_fc.add(Dropout(0.5))
		self.model_fc.add(Dense(512, input_dim=512))
		self.model_fc.add(Activation('relu'))
		self.model_fc.add(BatchNormalization())
		self.model_fc.add(Dropout(0.5))
		self.model_fc.add(Dense(256, input_dim=512))
		self.model_fc.add(Activation('relu'))
		self.model_fc.add(Dropout(0.3))
		self.model_fc.add(Dense(63, input_dim=64))
		self.model_fc.compile(optimizer='Adam', loss='mse')
	def train(self, features, labels, batch_size=512, epochs=4, verbose=1, validation_split=0.2):
		self.model_fc.fit(features, labels, batch_size=batch_size, epochs=epochs, verbose=verbose, validation_split=validation_split)

def build_model_from_data(features, labels, seq_length):
	dense_model = Dense_Module(seq_length)
	dense_model.train(features, labels)
	return dense_model.model

def overlap_samples(seq_length, feats, labels):
    new_l = labels[seq_length - 1:]
    feat_list = [feats[i:i + seq_length] for i in range(feats.shape[0] - seq_length + 1)]
    new_f = np.array(feat_list)
    return new_f, new_l

class NeuroML:
	def __init__(self, seq_length=24):
		self.model = None
		self.seq_length = seq_length
		self.q = deque()
		self.has_model = False
	def load_model(self, file_path):
		self.model = tf.keras.models.load_model(file_path)
		self.has_model = True
	def save_model(self, file_path):
		self.model.save(file_path)
	def build_model(self, joint_data_set, seq_length):
		df = pd.read_csv(joint_data_set)
		feature_ar = df.loc[:, 'ch1':'ch8'].values
		label_ar = df.loc[:, 'Wrist x':].values
		features, labels = overlap_samples(seq_length, feature_ar, label_ar)
		self.model = build_model_from_data(features, labels, seq_length)
		self.has_model = True
	def predict_sequence(self, sequence):
		if not self.has_model:
			raise RuntimeError("Model has not been defined")
		return self.model.predict(sequence)
	def predict(self, data):
		if not self.has_model:
			raise RuntimeError("Model has not been defined")
		self.q.append(np.array(data, dtype='float64'))
		if len(self.q) > self.seq_length:
			self.q.popleft()
			return self.model.predict(np.array(self.q).reshape([1, self.seq_length, 8]))[0]

if __name__ == '__main__':
	import sys
	import os
	if len(sys.argv) != 2:
		print('usage: neuro_ml.py joined_training_data')
		exit()
	print(tf.__version__)
	print ('Running Test:')
	ml = NeuroML()
	ml.build_model(sys.argv[1], 32)
	os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'    # Required for NFS setup
	ml.save_model('model.h5')