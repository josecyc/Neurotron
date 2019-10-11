import csv
import pandas as pd
import time

def add_cols(filename):
    df = pd.read_csv(filename)
    df.columns = ['ts', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8']
    df.to_csv(filename, index=False)

def write_to_csv(emg, args):
    with open('emg_data_{}_{}.csv'.format(args.name, args.nbr), 'a') as fd:
        writer = csv.writer(fd)
        emg = list(emg)
        emg.insert(0, time.time())
        writer.writerow(emg)