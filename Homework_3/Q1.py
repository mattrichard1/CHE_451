import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.optimize import fsolve

F = 0.085   # m^3 / min
V = 2.1     # m^3
k = 0.5     # m^3 / (mol * min)
Caos = 1.5  # mol / m^3
# Cas = 0.5   # mol / m^3

def tau(Cas):   # min
    y = V / (F + 2 * V * k * Cas)
    return y
def kp(Cas):    # unitless
    y = F / (F + 2 * V * k * Cas)
    return y


def Ca_analyt(t, Cao_prime, Cas):
    y = Cao_prime * kp(Cas) * (1 - np.exp(-t/tau(Cas)))
    return y

def part_a_ans(step, Cao_prime, Cas):
    error = 1.0
    tol = 1e-10
    t = 1.0
    Ca_prime = 0
    while error >= abs(tol):
        Ca_prime_new = Ca_analyt(t, Cao_prime, Cas)
        t = t + step
        error = abs(Ca_prime_new - Ca_prime) / Ca_prime_new
        Ca_prime = Ca_prime_new
    print(t, Ca_prime)
    return t, Ca_prime


for Cas in (0.1, 0.5, 0.75):
    part_a_ans(0.1, 1, Cas)