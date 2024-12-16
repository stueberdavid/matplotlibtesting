import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot(log_file1, log_file2, log_file3):
    # CSV-Datei einlesen und CPU-Nutzung extrahieren
    data1 = pd.read_csv(log_file1, delimiter=";")
    data2 = pd.read_csv(log_file2, delimiter=";")
    data3 = pd.read_csv(log_file3, delimiter=";")

    cpu_usage_data1 = data1["CPU(%)"].values  # CPU-Nutzungswerte in Prozent
    cpu_usage_data2 = data2["CPU(%)"].values  # CPU-Nutzungswerte in Prozent
    cpu_usage_data3 = data3["CPU(%)"].values  # CPU-Nutzungswerte in Prozent

    # Schritt 1: Sortiere die CPU-Auslastungsdaten
    sorted_cpu_data1 = np.sort(cpu_usage_data1)
    sorted_cpu_data2 = np.sort(cpu_usage_data2)
    sorted_cpu_data3 = np.sort(cpu_usage_data3)

    # Schritt 2: Berechne die CDF-Werte für die Y-Achse
    y_cdf1 = np.arange(1, len(sorted_cpu_data1) + 1) / len(sorted_cpu_data1)
    y_cdf2 = np.arange(1, len(sorted_cpu_data2) + 1) / len(sorted_cpu_data2)
    y_cdf3 = np.arange(1, len(sorted_cpu_data3) + 1) / len(sorted_cpu_data3)

    # Schritt 3: Erstellen des CDF-Plots
    plt.figure(figsize=(8, 5))
    plt.plot(sorted_cpu_data1, y_cdf1, marker=".", linestyle="--", color="b", label="Download")
    plt.plot(sorted_cpu_data2, y_cdf2, marker=".", linestyle="--", color="y", label="Upload")
    plt.plot(sorted_cpu_data3, y_cdf3, marker=".", linestyle="--", color="g", label="Download (Filter jedes 2. Paket")
    plt.xlabel("CPU-Auslastung (%)")
    plt.ylabel("Kumulative Wahrscheinlichkeit")
    plt.title("CDF der CPU-Auslastung für den Dumpcap-Prozess")
    plt.grid()
    plt.show()

plot("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 1 - Download/receiver_resource_usage.csv",
            "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 2 - Upload/receiver_resource_usage.csv",
            "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 3 - Donwload mit Filter (jedes 2. Paket)/receiver_resource_usage.filter.csv"
)