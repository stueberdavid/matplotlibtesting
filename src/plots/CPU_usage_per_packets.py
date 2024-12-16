from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scapy.utils import rdpcap

from plots.test import timestamps

CPU_Usage_File_Download = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 1 - Download/receiver_resource_usage.csv"
CPU_Usage_File_Upload = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 2 - Upload/receiver_resource_usage.csv"
CPU_Usage_File_Download_filter = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 3 - Donwload mit Filter (jedes 2. Paket)/receiver_resource_usage.filter.csv"

# PCAP-Datei laden

pcap1 =  rdpcap("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 1 - Download/test.pcap")
pcap2 =  rdpcap("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 2 - Upload/test.pcap")
pcap3 =  rdpcap("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 3 - Donwload mit Filter (jedes 2. Paket)/test.filter.pcap")

df1 = pd.read_csv(CPU_Usage_File_Download, sep=";")
df2 = pd.read_csv(CPU_Usage_File_Upload, sep=";")
df3 = pd.read_csv(CPU_Usage_File_Download_filter, sep=";")

CPU1 = df1["CPU(%)"].values
CPU2 = df2["CPU(%)"].values
CPU3 = df3["CPU(%)"].values

seconds_in_CPU_Usage1 = df1["Time in Milliseconds since Epoche"].values
seconds_in_CPU_Usage2 = df2["Time in Milliseconds since Epoche"].values
seconds_in_CPU_Usage3 = df3["Time in Milliseconds since Epoche"].values

def result(seconds_in_cpu_usage, pcapFile):
    result = []
    for i in range(len(seconds_in_cpu_usage)):
        result.append(0)

    # Zeitstempel extrahieren
    timestamps = [packet.time for packet in pcapFile]

    for timestamp in timestamps:
        for second in range(len(seconds_in_CPU_Usage1)):
            if np.round(int(seconds_in_cpu_usage[second] / 1000000000)) == int(timestamp):
                result[second] += 1

    return result

result1 = result(seconds_in_CPU_Usage1, pcap1)
result2 = result(seconds_in_CPU_Usage2, pcap2)
result3 = result(seconds_in_CPU_Usage3, pcap3)

print("result2:", result2)

y1= list(map(float, CPU1))
y2= list(map(float, CPU2))
y3= list(map(float, CPU3))

max_length = max(len(y1), len(y2), len(y3))

y1.extend([0] * (max_length - len(y1)))
y2.extend([0] * (max_length - len(y2)))
y3.extend([0] * (max_length - len(y3)))

result1.extend([0] * (max_length - len(result1)))
result2.extend([0] * (max_length - len(result2)))
result3.extend([0] * (max_length - len(result3)))


for i in range(len(y1)):
    if(result1[i] > 0):
        y1[i] = y1[i]/result1[i]

    else:
        y1[i] = 0

for i in range(len(y1)):
    if(result2[i] > 0):
        y2[i] = y2[i] / result2[i]
    else:
        y2[i] = 0

for i in range(len(y1)):
    if(result3[i] > 0):
        y3[i] = y3[i] / result3[i]
    else:
        y3[i] = 0


x = list(range(1, max_length + 1))

plt.figure(figsize=(8, 5))  # Optional: Größe des Plots anpassen
plt.plot(x, y1, marker='.', linestyle='-', color='g', label='Download')
plt.plot(x, y2, marker='.', linestyle='-', color='r', label='Upload')
plt.plot(x, y3, marker='.', linestyle=':', color='b', label='Download jedes 2. Paket')

# Achsenbeschriftung und Titel
plt.xlabel('Sekunden seit Messbeginn')
plt.ylabel('CPU Auslastung in % / Paketanzahl')
plt.title('CPU Auslastung pro Paket über die Zeit')
plt.legend()

# Plot anzeigen
plt.grid(True)
plt.show()


def plt_PaketeProSec(dataFrame):
    dataFrame['frame.time_epoch'] = dataFrame['frame.time_epoch'].astype(int)
    return dataFrame.groupby('frame.time_epoch').size().tolist()