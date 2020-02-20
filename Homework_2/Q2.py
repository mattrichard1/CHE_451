import matplotlib.pyplot as plt
import csv
import numpy as np

F = 0.085   #m^3 / min
V = 2.1     #m^3
kp = 1

def T_prime(t):
    tau = V / F
    y = kp * To_prime * (1 - np.exp( -t / tau))
    return y

