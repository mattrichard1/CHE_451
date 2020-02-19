import matplotlib.pyplot as plt
import csv

tau = 5 #min
CA0 = 20 #mol / L
k = 0.12 #min^-1

def R1A(CA1):
    y = 1 / tau * (CA0 - CA1) - k * CA1
    return y
def R1B(CA1, CB1):
    y = -1 / tau * CB1 + k * CA1
    return y
def R2A(CA1, CA2):
    y = 1 / tau * (CA1 - CA2) - k * CA2
    return y
def R2B(CB1, CB2, CA2):
    y = 1 / tau * (CB1 - CB2) + k * CA2
    return y


def Euler(concA, concB, step):
    t = 0.0
    tol = 1e-4
    time_list = [t]
    concA_list = [concA]
    concB_list = [concB]
    error = 1

    while t <= 5.0:
        concA_new = concA + R1A(concA) * step
        concB_new = concB + R1B(concA, concB) * step
        concA = concA_new
        concB = concB_new
        concA_list.append(concA)
        concB_list.append(concB)
        t = t + step
        time_list.append(t)
    concA1 = concA
    concB1 = concB

    while error >= abs(tol):
        concA_new = concA + R2A(concA1, concA) * step
        concB_new = concB + R2B(concB1, concB, concA) * step
        errorA = abs(concA_new - concA) / concA_new
        errorB = abs(concB_new - concB) / concB_new
        error = (errorA + errorB) / 2
        concA = concA_new
        concB = concB_new
        concA_list.append(concA)
        concB_list.append(concB)
        t = t + step
        time_list.append(t)
    print("Time to reach steady state:", t, "minutes")
    return [time_list, concA_list, concB_list]


steadystate = Euler(20, 0, 0.5)

with open('Q2ans.csv', 'w', newline='') as ans:
    wr = csv.writer(ans)
    wr.writerow(["Time (minutes)", "Conc A (mol / L)", "Conc B (mol / L)"])
    for i in range(len(steadystate[0])):
        wr.writerow([steadystate[0][i], steadystate[1][i], steadystate[2][i]])

plt.plot(steadystate[0], steadystate[1], label="A")
plt.plot(steadystate[0], steadystate[2], label="B")

plt.xlabel("Time (min)")
plt.ylabel("Molarity (mol / L)")
plt.title("Molarity of System Start-up Reaching Steady State \n Modelling A ----> B")
plt.legend(title="Reactants:")
plt.show()