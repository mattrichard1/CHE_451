import csv

with open("Temp_Data.csv", "r", newline='') as data:
    rd = csv.reader(data, delimiter='\t')
    print(

with open('Averaged_Data.csv', 'w', newline='') as avg:
    wr = csv.writer(avg)
    wr.writerow(["Time(sec)",	"Level",	"Setpoint",	"%Valve Output",	"Temp.",	"Setpoint",	"%Power to Heater"])
