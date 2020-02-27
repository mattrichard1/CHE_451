import matplotlib.pyplot as plt
import csv
import numpy as np

F = 0.085   # m^3 / min
V = 2.1     # m^3
k = 0.5     # m^3 / (mol * min)

Cao_s = 1       # mol / m^3
Cao_prime = 1   # mol / m^3
Ca_s = 0.1        # mol / m^3


#Part A; Analytical Solution:
def tau(F):
    y = V / (F + 2*V*k*Ca_s)
    return y
def kp(F):
    y = F / (F + 2*V*k*Ca_s)
    return y

def Ca_prime_analyt(t, F):
    y = Cao_prime * kp(F) * (1 - np.exp(-t / tau(F)))
    return y


#Part B; Numerical Solution & Graphical Comparison:
def dCa_prime_dt(Ca, F):
    y = F / V * (Cao_prime - (Ca - Ca_s)) - k * (Ca**2 - Ca_s**2)
    return y

def steady_state(step, F):
    tol = 1e-5
    error = 1

    t = 0
    tau_counter = t / tau(F)
    Ca_prime_a = 0
    Ca_prime_e = 0

    tau_list = [tau_counter]
    time_list = [t]
    Ca_prime_a_list = [Ca_prime_a]
    Ca_prime_e_list = [Ca_prime_e]
    Cao_prime_list = [0]
    diff_list = [0]

    while error >= abs(tol):
        # Analytical Method:
        Ca_prime_a_new = Ca_prime_analyt(t, F)
        error_a = abs(Ca_prime_a_new - Ca_prime_a) / Ca_prime_a_new
        if t == 0:
            error_a = 1
        Ca_prime_a = Ca_prime_a_new
        Ca_prime_a_list.append(Ca_prime_a)

        # Euler's Method:
        Ca_prime_e_new = Ca_prime_e + dCa_prime_dt(Ca_prime_e, F) * step
        error_e = abs(Ca_prime_e_new - Ca_prime_e) / Ca_prime_e_new
        if t == 0:
            error_e = 1
        Ca_prime_e = Ca_prime_e_new
        Ca_prime_e_list.append(Ca_prime_e)

        # Time Iterations
        t = t + step
        time_list.append(t)
        tau_counter = t / tau(F)
        tau_list.append(tau_counter)

        # Other:
        Cao_prime_list.append(Cao_prime)
        difference = abs(Ca_prime_e - Ca_prime_a)
        diff_list.append(difference)
        error = (error_a + error_e) / 2
    return(tau_list, time_list, Ca_prime_a_list, Ca_prime_e_list, Cao_prime_list, diff_list,
           tau_counter, t, Ca_prime_a, Ca_prime_e, difference)

with open('Q1ans.csv', 'w', newline='') as ans:
    wr = csv.writer(ans)
    wr.writerow(["Flow Rate (m^3 / min)", "Tau's", "Time (min)", "Ca'_analyt", "Ca'_euler", "difference in Ca'from models"])

test_range = [0.085, 1e-5, 0.01, 0.1, 0.25, 0.5, 1, 2, 5, 10]
for Flow in (test_range):
    compare = steady_state(0.1, Flow)

    with open('Q1ans.csv', 'a', newline='') as ans:
        wr = csv.writer(ans)
        wr.writerow([Flow, compare[6], compare[7], compare[8], compare[9], compare[10]])
    print("With a Flow Rate of:", Flow, "m^3 / min:")
    print("Analytical method concentration:", compare[8], "mol / m^3")
    print("Numerical method concentraction:", compare[9], "mol / m^3")
    print("Difference in methods:", compare[10], "mol / m^3")
    plt.plot(compare[0], compare[5], label=Flow)
plt.xlabel("Tau (min)")
plt.ylabel("Difference between modelling methods")
plt.legend(title="Flow Rates (m^3 / min):")
plt.show()


ans = steady_state(0.1, F)

plt.plot(ans[1], ans[2], label="Analytical model", color="k")
plt.plot(ans[1], ans[3], label="Numerical model", color="g")
plt.plot(ans[1], ans[4], label="Feed Stream", color="b")
plt.legend(title="Modeling Method")
plt.xlabel("Time (min)")
plt.ylabel("Deviation Concentration of A (mol / m^3)")
plt.show()