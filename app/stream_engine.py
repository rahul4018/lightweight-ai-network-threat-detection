import pandas as pd
import time
import random

def stream_packets(df, batch_size=50):

    total = len(df)
    index = 0

    while index < total:
        batch = df.iloc[index:index+batch_size]
        index += batch_size

        yield batch
        time.sleep(0.4)   # simulate network delay


def inject_noise(df):
    """simulate random attack spikes"""

    df = df.copy()

    spike_index = random.sample(range(len(df)), int(len(df)*0.03))

    df.loc[spike_index, "src_bytes"] *= 5
    df.loc[spike_index, "dst_bytes"] *= 4

    return df