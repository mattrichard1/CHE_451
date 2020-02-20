import matplotlib.pyplot as plt
import csv
import numpy as np

F = 0.085   # m^3 / min
V = 2.1     # m^3
k = 0.5     # m^3 / (mol * min)
Caos = 0.5  # mol / m^3
Cas = Caos  # mol / m^3


def analyt(t, Cao_prime):
    tau = V / (F + 2 * V * k * Cas)  # min
    kp = F / (F + 2 * V * k * Cas)   # unitless

    y = Cao_prime * kp * (1 - np.exp(-t/tau))
    return y

def partA_ans(Cao_prime):
    error = 1
    t = 0
    time_list = [t]

    while error > 1e-8:
        analyt(t, Cao_prime)
