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
    t = 0.01
    Ca_prime_a = 0  # Ca_prime_a is a deviation variable of Ca for analyt soln
    Ca_prime_n = 0  # Ca_prime_n is a deviation variable of Ca for num soln
    tol = 1e-5
    error = 1
    time_list = [t]
    analyt_list = [Ca_prime_a]
    numerical_list = [Ca_prime_n]
    Cao_prime_list = [0]

    while error >= abs(tol):
        # Feed data:
        Cao_prime_list.append(Cao_prime)

        # Analytical loop:
        analyt_new = Ca_dev_analyt(t)
        error_a = abs(analyt_new - Ca_prime_a) / analyt_new
        Ca_prime_a = analyt_new
        analyt_list.append(Ca_prime_a)

        #Numerical loop:
        num_new = Ca_prime_n + dCa_dt(Ca_prime_n) * step
        error_n = abs(num_new - Ca_prime_n) / num_new
        Ca_prime_n = num_new
        numerical_list.append(Ca_prime_n)
        error = (error_a + error_n) / 2

        time_list.append(t)
        t = t + step
    print("Steady state for analytical method:", t, "minutes", ",", Ca_prime_a, "mol / m^3")
    print("Steady state for numerical method:", t, "minutes", ",", Ca_prime_n, "mol / m^3")
    return [time_list, analyt_list, numerical_list, Cao_prime_list]


steadystate = Euler(0.1)

with open('Q1ans.csv', 'w', newline='') as ans:
    wr = csv.writer(ans)
    wr.writerow(["Time (minutes)", "Ca_analytical approx (mol / m^3)", "Ca_numerical approx (mol / m^3)"])
    for i in range(len(steadystate[0])):
        wr.writerow([steadystate[0][i], steadystate[1][i], steadystate[2][i]])



plt.plot(steadystate[0], steadystate[1], label="Analytical model", color="k")
plt.plot(steadystate[0], steadystate[2], label="Numerical model", color="g")
plt.plot(steadystate[0], steadystate[3], label="Feed Stream", color="b")
plt.legend(title="Modeling Method")
plt.xlabel("Time (min)")
plt.ylabel("Deviation Concentration of A (mol / m^3)")
plt.show()