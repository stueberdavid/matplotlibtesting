import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def dataPrepare(CPU_data_per_Second: list[float]):
    average_CPU_per_intervall = []  # Hier speichern wir die Durchschnitte der 5 Werte
    i = 0  # Index der Liste

    while i + 5 <= len(CPU_data_per_Second):  # Sicherstellen, dass genug Werte für einen Durchschnitt vorhanden sind
        # Ignoriere 1 Wert
        i += 1

        # Berechne den Durchschnitt der nächsten 5 Werte
        werte = CPU_data_per_Second[i:i + 5]
        durchschnitt = sum(werte) / len(werte)
        average_CPU_per_intervall.append(durchschnitt)

        # Ignoriere 3 weitere Werte
        i += 5 + 3

    return average_CPU_per_intervall

CPU_Usage_File_ALL = "/home/david/receiver_resource_usage.csv"
CPU_Usage_File_DOWNLOAD = "/home/david/receiver_resource_usage.down.csv"
CPU_Usage_File_Download_filter = "/home/david/receiver_resource_usage.up.csv"

df1 = pd.read_csv(CPU_Usage_File_ALL, sep=";")
df2 = pd.read_csv(CPU_Usage_File_DOWNLOAD, sep=";")
df3 = pd.read_csv(CPU_Usage_File_Download_filter, sep=";")

CPU1 = df1["CPU(%)"].values.tolist()
CPU2 = df2["CPU(%)"].values.tolist()
CPU3 = df3["CPU(%)"].values.tolist()

y1= dataPrepare(CPU1)
y2= dataPrepare(CPU2)
y3= dataPrepare(CPU3)

max_length = max(len(y1), len(y2), len(y3))

y1.extend([0] * (max_length - len(y1)))
y2.extend([0] * (max_length - len(y2)))
y3.extend([0] * (max_length - len(y3)))

x_values = np.logspace(0, 3, num=15)*100  # 10^0 = 1 bis 10^3 = 1000
input_x_values = np.round(x_values).astype(int)


plt.figure(figsize=(8, 5))  # Optional: Größe des Plots anpassen
plt.plot(x_values, y1, marker='.', linestyle=':', color='g', label='All traffic')
plt.plot(x_values, y2, marker='.', linestyle='-', color='r', label='Download')
#plt.plot(x_values, y3, marker='.', linestyle='--', color='b', label='Upload')

# Achsenbeschriftung und Titel
plt.xscale('log')
plt.xlabel('Senderate in kbits')
plt.ylabel('CPU Auslastung in %')
plt.title('CPU Auslastung über die Senderate')
plt.legend()

# Plot anzeigen
plt.grid(True)
plt.show()
