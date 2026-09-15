import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def model(y, t, k):
    dydt = -k * y
    return dydt

y0 = 5
t = np.linspace(0, 20, 100)
k = 0.3

y = odeint(model, y0, t, args=(k,))

print(y[:5])