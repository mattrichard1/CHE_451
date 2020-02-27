import csv
import numpy as np

with open("New_Bed_Height.csv", "r", newline='') as data:
    rd = csv.reader(data, delimiter='\t')
    next(rd)
    next(rd)

    time_list = []
    level_list = []
    temp_list = []
    power_to_heater_list = []

    data_points = 0
    time = 0
    while data_points < 5e3:
        counter = 0
        level_data = []
        temp_data = []
        power_data = []
        for row in rd:
            if counter > 9:
                time_list.append(time)
                time += 1
                level_list.append(level_avg)
                temp_list.append(temp_avg)
                power_to_heater_list.append(heater_avg)
                break

            level_numbers = float(row[1])
            level_data.append(level_numbers)
            level_avg = np.average(level_data)

            temp_numbers = float(row[4])
            temp_data.append(temp_numbers)
            temp_avg = np.average(temp_data)

            heater_numbers = float(row[6])
            power_data.append(heater_numbers)
            heater_avg = np.average(power_data)

            counter += 1
        data_points += 1




    with open('Averaged_Data.csv', 'w', newline='') as avg:
        wr = csv.writer(avg)
        wr.writerow(["Time(sec)", "Level (cm)", "Temp. (*C)", "% Power to Heater"])
        for i in range(len(time_list)):
            wr.writerow([time_list[i], level_list[i], temp_list[i], power_to_heater_list[i]])


# print("Time:", time_list)
# print("Temp:", temp_list)
# print("Level:", level_list)