import matplotlib.pyplot as plt
import pandas as pd


def dataPrepare(CPU_data_per_Second):
    # Anzahl der Datensätze (60) und Punkte pro Datensatz (50)
    num_datasets = 60
    points_per_dataset = 50

    # Datensätze in Blöcke zerlegen und die relevanten 50 Werte extrahieren
    prepared_data = []
    for k in range(num_datasets):
        start = k * 62 + 5  # Ignoriere die ersten 5 Werte jedes Blocks
        end = start + points_per_dataset  # Nimm die nächsten 50 Werte
        prepared_data.append(CPU_data_per_Second[start:end])


    return prepared_data


# CSV-Datei laden
CPU_Usage_File_ALL = "/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Longtesting - 60sec x 60repeats/test.csv"
df1 = pd.read_csv(CPU_Usage_File_ALL, sep=";")
CPU1 = df1["CPU(%)"].values.tolist()

print(len(CPU1))

# Daten vorbereiten
y1 = dataPrepare(CPU1)

# X-Achse: 1 bis 50
input_x_values = list(range(1, 51))

# Plotten der 60 Datensätze
plt.figure(figsize=(12, 8))  # Größeren Plot für Übersichtlichkeit
for dataset in y1:
    plt.plot(input_x_values, dataset, marker='.', linestyle=':', label='Datensatz')

# Achsenbeschriftung und Titel
plt.xlabel('Messpunkte (1-50)')
plt.ylabel('CPU-Auslastung (%)')
plt.title('CPU-Auslastung für 60 Datensätze')
plt.grid(True)
plt.show()
