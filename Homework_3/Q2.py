import matplotlib.pyplot as plt
import csv
import numpy as np

F = 0.085           # m^3 / min
V = 2.1             # m^3
rho = 1e3           # kg / m^3
T_s = 303           # K
Tc = T_s            # K
Cp = 1              # kcal / (kg * K)
Cao = 1             # mol / m^3
Ca_s = 0.075        # mol / m^3
UA = 65             # kcal / (min * K)
dH_rxn = -1300      # kcal / mol

A = 1e10        # min^-1
Ea = 59750      # J / mol
R = 8.314       # J / (mol * K)
def k(T):
    y = A * np.exp( -Ea / (R * T))
    return y


def dT_dt(T, Ca, To):
    y = F / V * (To - T) + ( (-dH_rxn*k(T)*V*Ca - UA*(T - Tc)) / (rho * V * Cp))
    return y

def dCa_dt(Ca, T):
    y = F / V * (Cao - Ca) - k(T) * Ca
    return y


def steady_state(step, To_prime):
    tol = 1e-7
    error = 1.0

    t = 0.0
    T = T_s
    Ca = Ca_s
    To = T_s + To_prime

    time_list = [t]
    T_list = [T_s]
    To_list = [T_s]
    Ca_list = [Ca_s]

    while error >= abs(tol):
        # Euler's Method:
        Ca_new = Ca + dCa_dt(Ca, T) * step
        error_c = abs(Ca_new - Ca) / Ca_new
        if t == 0:
            error_c = 1
        Ca = Ca_new

        T_new = T + dT_dt(T, Ca, To) * step
        error_t = abs(T_new - T) / T_new
        if t == 0:
            error_t = 1.0
        T = T_new

        # Data Storage:
        t = t + step
        time_list.append(t)
        Ca_list.append(Ca)
        T_list.append(T)
        To_list.append(To)

        error = (error_t + error_c) / 2

    return(time_list, Ca_list, T_list, To_list)

ans_B = steady_state(0.01, 20.0)

ans_C = steady_state(0.01, -20.0)

plt.plot(ans_B[0], ans_B[2], label='Tank Temp', color="k")
plt.plot(ans_B[0], ans_B[3], label='Feed Temp', color="g")
plt.legend(title="Stream Type:")
plt.xlabel("Time (min)")
plt.ylabel("Temp (K)")
plt.show()

plt.plot(ans_B[0], ans_B[1], label='Ca in outlet', color="k")
plt.legend(title="Concentration:")
plt.xlabel("Time (min)")
plt.ylabel("Concentration of A (mol / m^3)")
plt.show()

plt.plot(ans_C[0], ans_C[2], label='Tank Temp', color="k")
plt.plot(ans_C[0], ans_C[3], label='Feed Temp', color="g")
plt.legend(title="Stream Type:")
plt.xlabel("Time (min)")
plt.ylabel("Temp (K)")
plt.show()

plt.plot(ans_C[0], ans_C[1], label='Ca in outlet', color="k")
plt.legend(title="Concentration:")
plt.xlabel("Time (min)")
plt.ylabel("Concentration of A (mol / m^3)")
plt.show()