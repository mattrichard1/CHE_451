import matplotlib.pyplot as plt
import csv
import numpy as np

m_flow = 2.277566   # g / s
rho = 2.7           # g / cm^3
F = m_flow / rho    # cm^3 / s
V = 501.6404        # cm^3
To = 42.473         # °C
m_sys = 663.6702549 # g
U = 2.0e-4          # W / (cm^2 * °C) (assumption)
A = 480             # cm^2 (assumption)
Cp = 1550           # J / (g * °C) (general approximation)

def dT_dt(T):
    y = (F / V - (U*A - Cp*m_sys)/(rho*V*Cp)) * (To - T)
    return y

def steady_state(step):
    tol = 1e-5
    error = 1.0

    t = 0.0
    T = 38.7

    time_list = [t]
    temp_list = [T]
    To_list = [T]

    while error >= abs(tol):
        # Euler's Method:
        T_new = dT_dt(T) * step + T
        t = t + step
        time_list.append(t)
        error = abs(T_new - T) / T_new
        if t == 0:
            error_e = 1.0
        T = T_new
        temp_list.append(T)
        To_list.append(To)

    return(time_list, temp_list, To_list, t)

ans = steady_state(0.01)

with open('data.csv', 'w', newline='') as data:
    wr = csv.writer(data)
    wr.writerow(["Time (min)", "Temp output (°C)", "Temp input (°C)"])

for i in range(len(ans[0])):
    with open('data.csv', 'a', newline='') as data:
        wr = csv.writer(data)
        wr.writerow([ans[0][i], ans[1][i], ans[2][i]])

plt.plot(ans[0], ans[1])
plt.plot(ans[0], ans[2])
plt.xlabel("Time (min)")
plt.ylabel("Temp (°C)")
plt.show()