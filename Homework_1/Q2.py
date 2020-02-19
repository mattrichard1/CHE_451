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


def Euler(concA1, concB1, concA2, concB2, step):
    t = 0.0
    tol = 1e-4
    time_list = [t]
    concA1_list = [concA1]
    concB1_list = [concB1]
    concA2_list = [concA2]
    concB2_list = [concB2]
    error = 1

    while error >= abs(tol):
        concA1_new = concA1 + R1A(concA1) * step
        concB1_new = concB1 + R1B(concA1, concB1) * step
        concA2_new = concA2 + R2A(concA1, concA2) * step
        concB2_new = concB2 + R2B(concB1, concB2, concA2) * step
        errA1 = abs(concA1_new - concA1) / concA1_new
        errB1 = abs(concB1_new - concB1) / concB1_new
        errA2 = abs(concA2_new - concA2) / concA2_new
        errB2 = abs(concB2_new - concB2) / concB2_new
        error = (errA1 + errA2 + errB1 + errB2) / 4
        concA1 = concA1_new
        concB1 = concB1_new
        concA2 = concA2_new
        concB2 = concB2_new
        concA1_list.append(concA1)
        concB1_list.append(concB1)
        concA2_list.append(concA2)
        concB2_list.append(concB2)
        t = t + step
        time_list.append(t)
    print("Time to reach steady state:", t, "minutes")
    return [time_list, concA1_list, concB1_list, concA2_list, concB2_list]


steadystate = Euler(20, 0.0, 0.0, 1e-10, 0.5)

with open('Q2ans.csv', 'w', newline='') as ans:
    wr = csv.writer(ans)
    wr.writerow(["Time (minutes)", "Conc A1 (mol / L)", "Conc B1 (mol / L)", "Conc A2 (mol / L)", "Conc B2 (mol / L)"])
    for i in range(len(steadystate[0])):
        wr.writerow([steadystate[0][i], steadystate[1][i], steadystate[2][i], steadystate[3][i], steadystate[4][i]])

plt.plot(steadystate[0], steadystate[1], label="C_A1", color="b")
plt.plot(steadystate[0], steadystate[2], label="C_B1", color="g")
plt.plot(steadystate[0], steadystate[3], label="C_A2", color="c")
plt.plot(steadystate[0], steadystate[4], label="C_B2", color="k")

plt.xlabel("Time (min)")
plt.ylabel("Molarity (mol / L)")
plt.title("Molarity of System Start-up Reaching Steady State \n Modelling A ----> B")
plt.legend(title="Reactant concentrations:")
plt.show()