# ---------------------------------------------------------------------------- #
#  neuro_ml.py                                                                 #
#                                                                              #
#  By - jacksonwb                                                              #
#  Created: Sunday October 2019 7:22:07 pm                                     #
#  Modified: Sunday Oct 2019 7:48:26 pm                                        #
#  Modified By: jacksonwb                                                      #
# ---------------------------------------------------------------------------- #

from collections import deque
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model

class NeuroML:
	def __init__(self, seq_length=24):
		self.model = None
		self.seq_length = seq_length
		self.q = deque()
	def load_model(self, file_path):
		self.model = tensorflow.keras.models.load_model(file_path)
	def predict(self, data):
		self.q.append(np.array(data))
		if len(self.q > 24):
			self.q.popleft()
			return self.model.predict(np.array(self.q))

