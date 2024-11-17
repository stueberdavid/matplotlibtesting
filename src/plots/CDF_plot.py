import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


log_file = "/home/david/receiver_resource_usage.csv"

# CSV-Datei einlesen und CPU-Nutzung extrahieren
data = pd.read_csv(log_file, delimiter=";")
cpu_usage_data = data["CPU(%)"].values  # CPU-Nutzungswerte in Prozent

# Schritt 1: Sortiere die CPU-Auslastungsdaten
sorted_cpu_data = np.sort(cpu_usage_data)

# Schritt 2: Berechne die CDF-Werte für die Y-Achse
y_cdf = np.arange(1, len(sorted_cpu_data) + 1) / len(sorted_cpu_data)

# Schritt 3: Erstellen des CDF-Plots
plt.figure(figsize=(8, 5))
plt.plot(sorted_cpu_data, y_cdf, marker=".", linestyle="none", color="blue")
plt.xlabel("CPU-Auslastung (%)")
plt.ylabel("Kumulative Wahrscheinlichkeit")
plt.title("CDF der CPU-Auslastung für den Dumpcap-Prozess")
plt.grid()
plt.show()
