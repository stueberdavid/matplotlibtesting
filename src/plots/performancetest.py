import timeit
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



# Definieren der Funktionen außerhalb des zu messenden Codes
def plotten(input):
    daten = input[0]
    anzahl = input[1]
    x_achse = input[2]
    y_achse = input[3]

    x = anzahl
    y = daten

    plt.bar(x, y)

    plt.title('Datenauswertung von Versuch2.csv')
    plt.xlabel(x_achse)
    plt.ylabel(y_achse)

    plt.xlabel('Pakete über die Zeit')
    plt.ylabel('Größe der eingehenden Pakete')
    plt.grid(True)

    plt.show()

def plt_normal2(dateiname):

    versuch = pd.read_csv(dateiname)
    # Zeile gibt an in welcher Zeile der CSV Datei man sich befindet
    zeile = 0

    # intanzahl ist eine Laufvariable, die angibt wie viele Werte in der List 'daten' stehen und speichert diese in der
    # Liste 'Anzahl'
    intanzahl = 0

    # daten ist eine Liste, die immer die Paketgröße abspeichert, wenn ein Paket empfangen wurde
    daten = []

    # Anzahl ist eine Liste mit der Anzahl von der Liste 'daten'
    anzahl = []

    # iteriert über die CSV Datei und speichert die Länge der empfangenen Pakete in der Liste 'daten'
    for index, row in versuch.iterrows():
        if versuch.loc[zeile, 'ip.dst'] == '172.16.31.14':
            laenge = versuch.loc[zeile, 'frame.len']

            anzahl.append(intanzahl)
            intanzahl += 1
            daten.append(laenge)

        zeile += 1

    return daten, anzahl, 'Pakete über die Zeit', 'Größe der eingehenden Pakete'



# Der zu messende Code als String
code_to_test = """
input_data = plt_normal2('streamvergleich720p.csv')
plotten(input_data)
"""

# Zeit messen
elapsed_time = timeit.timeit(code_to_test, number=1, globals=globals())
print(f"Die Laufzeit beträgt {elapsed_time:.4f} Sekunden")