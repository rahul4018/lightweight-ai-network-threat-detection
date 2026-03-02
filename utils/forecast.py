import numpy as np

def forecast_risk(history):

    if len(history) < 5:
        return history[-1]

    trend = np.polyfit(range(len(history)), history, 1)
    next_value = trend[0]*len(history) + trend[1]

    return round(next_value,2)