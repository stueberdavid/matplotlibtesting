import matplotlib.pyplot as plt
import pandas as pd

CPU_Usage_File_Download = "/home/david/receiver_resource_usage.csv"
#CPU_Usage_File_Download = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 1 - Download/receiver_resource_usage.csv"
CPU_Usage_File_Upload = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 2 - Upload/receiver_resource_usage.csv"
CPU_Usage_File_Download_filter = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 3 - Donwload mit Filter (jedes 2. Paket)/receiver_resource_usage.filter.csv"

df1 = pd.read_csv(CPU_Usage_File_Download, sep=";")
df2 = pd.read_csv(CPU_Usage_File_Upload, sep=";")
df3 = pd.read_csv(CPU_Usage_File_Download_filter, sep=";")

CPU1 = df1["CPU(%)"].values
CPU2 = df2["CPU(%)"].values
CPU3 = df3["CPU(%)"].values

y1= list(map(float, CPU1))
y2= list(map(float, CPU2))
y3= list(map(float, CPU3))

max_length = max(len(y1), len(y2), len(y3))

y1.extend([0] * (max_length - len(y1)))
y2.extend([0] * (max_length - len(y2)))
y3.extend([0] * (max_length - len(y3)))

x = list(range(1, max_length + 1))

plt.figure(figsize=(8, 5))  # Optional: Größe des Plots anpassen
plt.plot(x, y1, marker='.', linestyle=':', color='g', label='Download')
#plt.plot(x, y2, marker='.', linestyle='-', color='r', label='Upload')
#plt.plot(x, y3, marker='.', linestyle='--', color='b', label='Download jedes 2. Paket')

# Achsenbeschriftung und Titel
plt.xlabel('Sekunden seit Messbeginn')
plt.ylabel('CPU Auslastung in %')
plt.title('CPU Auslastung über die Zeit')
plt.legend()

# Plot anzeigen
plt.grid(True)
plt.show()
