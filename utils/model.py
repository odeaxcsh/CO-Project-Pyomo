import numpy as np
from .data import intercept_bounds, slope_bounds

from pyomo.environ import *

def getx_rule(data):
    def getx(_, i):
        return data[i - 1, 0]
    return getx


def gety_rule(data):
    def gety(_, i):
        return data[i - 1, 1]
    return gety


def getM1_rule(data):
    intercepts, slopes = np.array(intercept_bounds(data)), np.array(slope_bounds(data))
    def getM1(model, i):
       return np.max(np.abs(model.Y[i] - slopes * model.X[i] + intercepts))
    return getM1


def getM2_rule(data):
    intercepts, slopes = np.array(intercept_bounds(data)), np.array(slope_bounds(data))
    def getM2(model, i):
       return intercepts[1] - intercepts[0] - model.X[i] * (slopes[0] - slopes[1])
    return getM2


def init_model(data):
    model = ConcreteModel()
    model.n = Param(initialize=data.shape[0])
    model.I = RangeSet(1, model.n)
    model.X = Param(model.I, initialize=getx_rule(data))
    model.Y = Param(model.I, initialize=gety_rule(data))
    return model
