import matplotlib.pyplot as plt
import csv
import numpy as np

F = 0.085   # m^3 / min
V = 2.1     # m^3
k = 0.5     # m^3 / (mol * min)

Cao_s = 1.0                 # mol / m^3
Cao_prime = 1.0             # mol / m^3
Cao = Cao_s + Cao_prime     # mol / m^3
Ca_s = 0.247                # mol / m^3


# Part A; Analytical Solution:
def tau(F):
    y = V / (F + 2*V*k*Ca_s)
    return y
def kp(F):
    y = F / (F + 2*V*k*Ca_s)
    return y

def Ca_prime_analyt(t, F):
    y = Cao_prime * kp(F) * (1 - np.exp(-t / tau(F)))
    return y



# Part B & C; Numerical Solution & Graphical Comparison:
def dCa_prime_dt(Ca_prime, F):
    y = (F / V) * (Cao_prime - Ca_prime) - k * Ca_prime**2
    return y

def steady_state(step, F):
    tol = 1e-5
    error = 1.0

    t = 0.0
    tau_counter = t / tau(F)
    Ca_prime_a = 0.0
    Ca_prime_e = 0.0

    tau_list = [tau_counter]
    time_list = [t]
    Ca_prime_a_list = [Ca_prime_a]
    Ca_prime_e_list = [Ca_prime_e]
    Cao_prime_list = [0.0]
    diff_list = [0.0]
    Ca_a_list = [Ca_s]
    Ca_e_list = [Ca_s]
    Cao_list = [Cao_s]

    while error >= abs(tol):
        # Analytical Method:
        Ca_prime_a_new = Ca_prime_analyt(t, F)
        error_a = abs(Ca_prime_a_new - Ca_prime_a) / Ca_prime_a_new
        if t == 0:
            error_a = 1.0
        Ca_prime_a = Ca_prime_a_new
        Ca_prime_a_list.append(Ca_prime_a)

        # Euler's Method:
        Ca_prime_e_new = Ca_prime_e + dCa_prime_dt(Ca_prime_e, F) * step
        error_e = abs(Ca_prime_e_new - Ca_prime_e) / Ca_prime_e_new
        if t == 0:
            error_e = 1.0
        Ca_prime_e = Ca_prime_e_new
        Ca_prime_e_list.append(Ca_prime_e)

        # Time Iterations:
        t = t + step
        time_list.append(t)
        tau_counter = t / tau(F)
        tau_list.append(tau_counter)

        # Other:
        Ca_a = Ca_s + Ca_prime_a
        Ca_e = Ca_s + Ca_prime_e
        Ca_a_list.append(Ca_a)
        Ca_e_list.append(Ca_e)
        Cao_prime_list.append(Cao_prime)
        Cao_list.append(Cao)
        difference = abs(Ca_prime_e - Ca_prime_a)
        diff_list.append(difference)
        error = (error_a + error_e) / 2.0

    return(tau_list, time_list, Ca_prime_a_list, Ca_prime_e_list, Cao_prime_list,
           diff_list, tau_counter, t, Ca_prime_a, Ca_prime_e,
           difference, Ca_a_list, Ca_e_list, Cao_list)


ans = steady_state(0.1, F)

plt.plot(ans[1], ans[11], label="Analytical model outlet", color="k")
plt.plot(ans[1], ans[12], label="Numerical model outlet", color="g")
plt.plot(ans[1], ans[13], label="Feed", color="b")
plt.legend(title="Stream Type:")
plt.xlabel("Time (min)")
plt.ylabel("Concentration of A (mol / m^3)")
plt.show()

plt.plot(ans[0], ans[11], label="Analytical model outlet", color="k")
plt.plot(ans[0], ans[12], label="Numerical model outlet", color="g")
plt.plot(ans[0], ans[13], label="Feed", color="b")
plt.legend(title="Stream Type:")
plt.xlabel("Tau")
plt.ylabel("Deviation Concentration of A (mol / m^3)")
plt.show()
print(ans[10])



# Part D; Comparing Analyt & Numerical Models Across Different Flows:
test_range = np.arange(0.0, 20 , 0.005)
for Flow in (test_range):
    compare = steady_state(0.1, Flow)
    plt.plot(Flow, compare[10], marker='o', color='black', markersize='1')
plt.xlabel("Flow Rate (m^3 / min)")
plt.ylabel("Difference between analytical and numerical \n (mol / m^3)")
plt.show()