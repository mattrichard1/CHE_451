import matplotlib.pyplot as plt
import csv

def drainrate(h):
    k = 0.075
    y = -k * h ** 0.5
    return y


def timetodrain(h, step):
    t = 0.0
    tol = 1e-10
    t_list = [t]

    h_list = [h]

    while h >= abs(tol):
        h_new = h + drainrate(h) * step
        t = t + step
        h = h_new
        t_list.append(t)
        h_list.append(h)

    return [t_list, h_list, step, t]


with open('Q1ans.csv', 'w', newline='') as ans:
    wr = csv.writer(ans)
    wr.writerow(["Step Size", "Drain Time (seconds)"])

with open('Q1data.csv', 'w', newline='') as data:
    wr = csv.writer(data)
    wr.writerow(["Time (seconds)", "Fluid Height (meters)"])


step_sizes = [5, 2, 1, 0.5, 0.1, 0.01, 1e-3, 1e-5]
step_sizes_data = [5, 2, 1, 0.1, 0.01]
for step in step_sizes:
    coords = timetodrain(2, step)

    with open('Q1ans.csv', 'a', newline='') as ans:
        wr = csv.writer(ans)
        wr.writerow([coords[2], coords[3]])
    plt.plot(coords[0], coords[1], label=step)
    print("With step size of", coords[2], ", time to drain:", coords[3], "seconds")

for step in step_sizes_data:
    with open('Q1data.csv', 'a', newline="") as data:
        wr = csv.writer(data)
        wr.writerow("")
    coords = timetodrain(2, step)
    for i in range(len(coords[0])):
        with open('Q1data.csv', 'a', newline='') as data:
            wr = csv.writer(data)
            wr.writerow([coords[0][i], coords[1][i]])


plt.xlabel("Time (s)")
plt.ylabel("Fluid Height (m)")
plt.title("Fluid Height Approximated Using\nEuler's Method with Varying Step Sizes")
plt.legend(title="Using a step size of:")
plt.show()