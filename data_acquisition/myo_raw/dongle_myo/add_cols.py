import sys
import pandas as pd

def main(filename):
    df = pd.read_csv(filename)
    df.columns = ['ts', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8']
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    main(sys.argv[1])
