import matplotlib.pyplot as plt
import pandas as pd
from scapy.all import rdpcap
from collections import defaultdict

# Dateien und PCAP laden
CPU_Usage_File_Download = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 1 - Download/receiver_resource_usage.csv"
CPU_Usage_File_Upload = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 2 - Upload/receiver_resource_usage.csv"
CPU_Usage_File_Download_filter = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 3 - Donwload mit Filter (jedes 2. Paket)/receiver_resource_usage.filter.csv"

df1 = pd.read_csv(CPU_Usage_File_Download, sep=";")
df2 = pd.read_csv(CPU_Usage_File_Upload, sep=";")
df3 = pd.read_csv(CPU_Usage_File_Download_filter, sep=";")

CPU1 = df1["CPU(%)"].values
CPU2 = df2["CPU(%)"].values
CPU3 = df3["CPU(%)"].values

seconds_in_CPU_Usage1 = df1["Time in Milliseconds since Epoche"].values
seconds_in_CPU_Usage2 = df2["Time in Milliseconds since Epoche"].values
seconds_in_CPU_Usage3 = df3["Time in Milliseconds since Epoche"].values


def analyze_pcap(file_path):
    # PCAP-Datei laden
    packets = rdpcap(file_path)

    # Dictionary für die Byte-Zählung pro Sekunde
    data_per_second = defaultdict(int)

    # Datenmenge pro Sekunde berechnen
    for packet in packets:
        # Zeitstempel des Pakets (in Sekunden, abgeschnitten)
        second = int(packet.time)
        # Größe des Pakets in Bytes
        data_per_second[second] += len(packet)

    # Ergebnisse in eine Liste umwandeln, sortiert nach Zeit
    sorted_data = sorted(data_per_second.items())
    result_list = [bytes_ for _, bytes_ in sorted_data]

    return result_list

# Durchsatz berechnen
throughput1 = analyze_pcap("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 1 - Download/test.pcap")
throughput2 = analyze_pcap("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 2 - Upload/test.pcap")
throughput3 = analyze_pcap("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 3 - Donwload mit Filter (jedes 2. Paket)/test.filter.pcap")

# CPU durch Durchsatz teilen
y1 = [cpu / t if t > 0 else 0 for cpu, t in zip(CPU1, throughput1)]
y2 = [cpu / t if t > 0 else 0 for cpu, t in zip(CPU2, throughput2)]
y3 = [cpu / t if t > 0 else 0 for cpu, t in zip(CPU3, throughput3)]

# Für gleich lange Listen auffüllen
max_length = max(len(y1), len(y3))
y1.extend([0] * (max_length - len(y1)))
y2.extend([0] * (max_length - len(y2)))
y3.extend([0] * (max_length - len(y3)))

x = list(range(1, max_length + 1))

# Plot
plt.figure(figsize=(8, 5))
plt.plot(x, y1, marker='.', linestyle='-', color='g', label='Download CPU/Durchsatz')
plt.plot(x, y2, marker='.', linestyle='-', color='r', label='Upload CPU/Durchsatz')
plt.plot(x, y3, marker='.', linestyle=':', color='b', label='Download mit Filter CPU/Durchsatz')

plt.xlabel('Sekunden seit Messbeginn')
plt.ylabel('CPU-Auslastung / Durchsatz')
plt.title('CPU-Auslastung normalisiert auf Durchsatz')
plt.legend()
plt.grid(True)
plt.show()








