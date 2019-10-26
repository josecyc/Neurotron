#! /usr/bin/env python3
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    join_csvs.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jackson <jbeall@student.42.us.org>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/06/17 20:30:17 by tholzheu          #+#    #+#              #
#    Updated: 2019/10/11 15:04:25 by jackson          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd
import numpy as np
import sys
import time
from datetime import datetime

def crop_dfs(leap_df, emg_df):
	"""Crops both DataFrames to start at the same time"""
	i = 0
	while (emg_df['ts'][i] < leap_df['Unix Time'][0]):
		i += 1
	i -= 1
	j = len(emg_df) - 1
	while (emg_df['ts'][j] > leap_df['Unix Time'][len(leap_df) - 1]):
		j -= 1
	j += 1
	return (leap_df, emg_df[i:j].reset_index(drop=True))

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("usage: join_csvs.py leap_data emg_data out_file")
		exit(1);
	leap_df = pd.read_csv(sys.argv[1])
	del(leap_df['Timestamp'])
	emg_df = pd.read_csv(sys.argv[2])
	emg_df.columns = ['ts', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8'] # this line should not be necessary
	print ("Cropping Dataframes")
	leap_df, emg_df = crop_dfs(leap_df, emg_df)

	rows = len(emg_df)
	columns = 74
	print('col len:', len(leap_df.columns) + len(emg_df.columns))
	length_leap = len(leap_df)
	combined = np.zeros((rows, columns))

	print ("Joining Dataframes...")
	j = 0
	k = 0
	i = 0
	while (i < rows):
		while (leap_df["Unix Time"][j] - emg_df["ts"][i] > 0.1):
			i += 1
		leap = leap_df.iloc[j].values
		count = 1
		j += 1
		while (j < length_leap and leap_df["Unix Time"][j] <= emg_df["ts"][i]):
			leap += leap_df.iloc[j].values
			j += 1
			count += 1
		leap /= count
		time_leap = leap[0]
		leap = leap[4:]
		emg = emg_df.iloc[i].values
		time_diff = time_leap - emg[0]
		combined[i] = np.concatenate([np.array([time_leap]), np.array([time_diff]), emg, leap])
		k += 1
		i += 1
	combined = combined[:k]

	print ("Converting to Dataframe...")
	column_names = ['Leap timestamp', 'timestamp diff', 'emg timestamp',
				'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8',
				'Wrist x', 'Wrist y', 'Wrist z', 'Thumb Proximal x', 'Thumb Proximal y',
				'Thumb Proximal z', 'Thumb Intermediate x', 'Thumb Intermediate y',
				'Thumb Intermediate z', 'Thumb Distal x', 'Thumb Distal y',
				'Thumb Distal z', 'Thumb Tip x', 'Thumb Tip y', 'Thumb Tip z',
				'Index Proximal x', 'Index Proximal y', 'Index Proximal z',
				'Index Intermediate x', 'Index Intermediate y', 'Index Intermediate z',
				'Index Distal x', 'Index Distal y', 'Index Distal z', 'Index Tip x',
				'Index Tip y', 'Index Tip z', 'Middle Proximal x', 'Middle Proximal y',
				'Middle Proximal z', 'Middle Intermediate x', 'Middle Intermediate y',
				'Middle Intermediate z', 'Middle Distal x', 'Middle Distal y',
				'Middle Distal z', 'Middle Tip x', 'Middle Tip y', 'Middle Tip z',
				'Ring Proximal x', 'Ring Proximal y', 'Ring Proximal z',
				'Ring Intermediate x', 'Ring Intermediate y', 'Ring Intermediate z',
				'Ring Distal x', 'Ring Distal y', 'Ring Distal z', 'Ring Tip x',
				'Ring Tip y', 'Ring Tip z', 'Pinky Proximal x', 'Pinky Proximal y',
				'Pinky Proximal z', 'Pinky Intermediate x', 'Pinky Intermediate y',
				'Pinky Intermediate z', 'Pinky Distal x', 'Pinky Distal y',
				'Pinky Distal z', 'Pinky Tip x', 'Pinky Tip y', 'Pinky Tip z']
	combined_df = pd.DataFrame(data=combined, columns=column_names)
	print ("Double check:")
	print (combined_df.describe()['timestamp diff'])
	name = "joined_data_{}_{}_{}.csv".format(len(combined_df), datetime.now().strftime("%d-%b-%y_%H:%M"), sys.argv[3])
	combined_df.to_csv(name, index=False)
	print ("Finished joining --> {}  size = {}".format(name, len(combined_df)))
