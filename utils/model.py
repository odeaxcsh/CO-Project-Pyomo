from pyomo.environ import *


def getx_rule(data):
    def getx(_, i):
        return data[i - 1, 0]
    return getx


def gety_rule(data):
    def gety(_, i):
        return data[i - 1, 1]
    return gety


def init_model(data):
    model = ConcreteModel()
    model.n = Param(initialize=data.shape[0])
    model.I = RangeSet(1, model.n)
    model.X = Param(model.I, initialize=getx_rule(data))
    model.Y = Param(model.I, initialize=gety_rule(data))
    return model
