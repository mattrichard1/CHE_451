import matplotlib.pyplot as plt
import csv
import numpy as np

F = 0.085   # m^3 / min
V = 2.1     # m^3
k = 0.5     # m^3 / (mol * min)

Cao_init = 0.925        # mol / m^3         (assumed value)
Cao_prime = 1       # mol / m^3
Cao = Cao_init + Cao_prime  # mol / m^3

Ca_init = 0.236         # mol / m^3         (assumed value)


#Part A; Analytical Solution:
tau = V / (F + 2*V*k*Ca_init)
kp = F / (F + 2*V*k*Ca_init)

def Ca_dev_analyt(t):
    y = Cao_prime * kp * (1 - np.exp(-t / tau))
    return y


#Part B; Numerical Solution & Graphical Comparison:
def dCa_dt(Ca):
    y = F / V * (Cao_prime - (Ca - Ca_init)) - k * (Ca**2 + Ca_init**2)
    return y

def Euler(step):
    t = 1.0
    Ca_prime_a = 0  # Ca_prime_a is a deviation variable of Ca for analyt soln
    Ca_prime_n = 0  # Ca_prime_n is a deviation variable of Ca for num soln
    tol = 1e-4
    error_a = 1
    error_n = 1
    time_list_a = [t]
    time_list_n = [t]
    analyt_list = [Ca_prime_a]
    numerical_list = [Ca_prime_n]

    #Analytical loop:
    while error_a >= abs(tol):
        analyt_new = Ca_dev_analyt(t)
        error_a = abs(analyt_new - Ca_prime_a) / analyt_new
        Ca_prime_a = analyt_new
        t = t + step
        time_list_a.append(t)
        analyt_list.append(Ca_prime_a)
    print("Steady state for analytical method:", t, "minutes", ",", Ca_prime_a, "mol / m^3")

    #Numerical loop:
    t = 1.0
    while error_n >= abs(tol):
        num_new = Ca_prime_n + dCa_dt(Ca_prime_n) * step
        error_n = abs(num_new - Ca_prime_n) / num_new
        Ca_prime_n = num_new
        t = t + step
        time_list_n.append(t)
        numerical_list.append(Ca_prime_n)
    print("Steady state for numerical method:", t, "minutes", ",", Ca_prime_n, "mol / m^3")

    return [time_list_a, time_list_n, analyt_list, numerical_list]

steadystate = Euler(0.1)

with open('Q1ans.csv', 'w', newline='') as ans:
    wr = csv.writer(ans)
    wr.writerow(["Time (minutes)", "Ca_analytical approx (mol / m^3)", "Ca_numerical approx (mol / m^3)"])
    for i in range(len(steadystate[0])):
        wr.writerow([steadystate[0][i], steadystate[2][i], steadystate[3][i]])

plt.plot(steadystate[0], steadystate[2], label="Analytical model")
plt.plot(steadystate[1], steadystate[3], label="Numerical model")
plt.legend(title="Modeling Method")
plt.show()