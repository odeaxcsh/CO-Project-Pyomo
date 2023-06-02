from pyomo.environ import *
from matplotlib import pyplot as plt

from utils.model import init_model
from utils.data import load_data, slope_bounds, intercept_bounds


data = load_data('Data/Paperweight.txt')

CL, CU = slope_bounds(data)
DL, DU = intercept_bounds(data)

model = init_model(data)

model.c = Var(bounds=(CL, CU))
model.d = Var(bounds=(DL, DU))

model.e = Var(model.I, domain=NonNegativeReals)


@model.Constraint(model.I)
def error_constraint_leq(model, i):
    return model.Y[i] - model.c * model.X[i] - model.d <= model.e[i]


@model.Constraint(model.I)
def error_constraint_geq(model, i):
    return model.Y[i] - model.c * model.X[i] - model.d >= -model.e[i]


model.obj = Objective(expr=sum(model.e[i] for i in model.I))

result = SolverFactory('glpk', tee=True).solve(model)

if result.solver.termination_condition != TerminationCondition.optimal:
    raise Exception('Solver did not find an optimal solution')


print(f'Objective: {model.obj():.2f}')
print(f'Solution: {model.c():.2f}x + {model.d():.2f} = y')

plt.scatter(data[:, 0], data[:, 1])
plt.plot(data[:, 0], model.c() * data[:, 0] + model.d(), color='red')
plt.show()
