import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def find_and_plot_uploadrates(base_dir):
    upload_rates = []

    # Durchlaufe alle Unterordner und Dateien
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "requests.csv":
                file_path = os.path.join(root, file)
                try:
                    # Lese die CSV-Datei ein
                    df = pd.read_csv(file_path)

                    # Überprüfen, ob die Spalte 'uploadrate' vorhanden ist
                    if 'uplinkBytes' in df.columns:
                        # Filtere ungültige Werte aus der Spalte
                        valid_rates = pd.to_numeric(df['uplinkBytes'], errors='coerce').dropna()
                        valid_rates = valid_rates[valid_rates >= 0]  # Nur nicht-negative Werte zulassen
                        upload_rates.extend(valid_rates.tolist())
                except Exception as e:
                    print(f"Fehler beim Verarbeiten der Datei {file_path}: {e}")

    if upload_rates:
        upload_rates = np.array(upload_rates)
        upload_rates = upload_rates[upload_rates > 0]  # Entferne Nullwerte, da log nicht definiert ist
        bins = np.logspace(np.log10(min(upload_rates)), np.log10(max(upload_rates)), 50)
        # Plot der Verteilung der Uploadraten
        plt.figure(figsize=(10, 6))
        plt.hist(upload_rates, bins=bins, edgecolor='black', alpha=0.7, density=True)
        plt.xscale('log')  # Logarithmische Skala auf der x-Achse
        plt.title('Verteilung der Upload bytes (logarithmisch)')
        plt.xlabel('Uploadrate (logarithmische Skala in Mbps)')
        plt.ylabel('Relative Häufigkeit')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
    else:
        print("Keine Uploadraten gefunden.")

if __name__ == "__main__":
    find_and_plot_uploadrates("/media/david/c6a80248-7aa3-42ce-b5ea-8ae505d37261/Logfiles/new_ds")