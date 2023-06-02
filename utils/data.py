import numpy as np


def load_data(filename):
    file = open(filename, 'r')
    if file is None:
        raise Exception('File not found: ' + filename)
    
    lines = file.readlines()
    data = [line.strip().split() for line in lines]
    data = np.array(data, dtype=np.float32)
    return data


def slope_bounds(data):
    x, y = data[:, 0], data[:, 1]
    slope_min = np.nanmin((y[:, None] - y[None, :]) / (x[:, None] - x[None, :]))
    slope_max = np.nanmax((y[:, None] - y[None, :]) / (x[:, None] - x[None, :]))
    return slope_min, slope_max


def intercept_bounds(data):
    x, y = data[:, 0], data[:, 1]
    extereme_slopes = np.array(slope_bounds(data))
    intercepts = y[:, None] - extereme_slopes * x[:, None]
    intercept_min = np.nanmin(intercepts)
    intercept_max = np.nanmax(intercepts)
    return intercept_min, intercept_max

