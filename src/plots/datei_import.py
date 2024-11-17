import os
import pandas as pd
from plots import pandasplot
import numpy as np
from matplotlib import pyplot as plt
import math

def plotueberordner (dateipfad):
    for filename in os.listdir(dateipfad):
        pandasplot.plt_normal(filename)


def plotueberordner_dateigroesse (dateipfad):
    zaehler = 0
    # zählt wie viele Datein in dem Ordner vorhanden sind
    for filename in os.listdir(dateipfad):
        zaehler += 1

    # Liste mit Indexing für plotten-aufruf
    daten_anzahl = np.arange(zaehler)

    # initialisierung der Liste für Performance
    daten = [None] * zaehler

    # Befüllung der Liste mit Daten
    # sorted() sortiert nicht wie gewünscht. Es sortiert die Zahlen nicht nach Größe
    for index, filename in enumerate(sorted(os.listdir(dateipfad))):
        full_path = os.path.join(dateipfad, filename, 'all_network_traffic.csv')
        daten[index] = os.stat(full_path).st_size


    plt.bar (daten_anzahl, daten)
    plt.xlabel('Nummer der Datei')
    plt.ylabel('Datei Größe der Datei in MB')


    plt.show()



def plotueberordner_downloadrate (dateipfad):
    zaehler = 0
    # zählt wie viele Datein in dem Ordner vorhanden sind
    for filename in os.listdir(dateipfad):
        zaehler += 1

    # initialisierung der  Liste für Performance
    daten = [0] * zaehler

    actzeitslot = 0

    # Befüllung der Liste mit Daten
    # sorted() sortiert nicht wie gewünscht. Es sortiert die Zahlen nicht nach Größe
    for index, filename in enumerate(sorted(os.listdir(dateipfad))):
        full_path = os.path.join(dateipfad, filename, 'all_network_traffic.csv')
        current_file_data = pd.read_csv(full_path)
        actzeit = math.floor(current_file_data.loc[index, 'timestamp'])
        for index1, row in current_file_data.iterrows():
            zeile = index1
            if current_file_data.loc[zeile, 'ipDst'] == '10.10.0.140':
                if actzeit == math.floor(current_file_data.loc[zeile, 'timestamp']):
                    if pd.isna(current_file_data.loc[zeile, 'udpLen']):
                        daten[index] += (current_file_data.loc[zeile, 'tcpLen'])
                    else:
                        daten[index] += current_file_data.loc[zeile, 'udpLen']

                else:
                    actzeit = math.floor(current_file_data.loc[zeile, 'timestamp'])
                    actzeitslot += 1
                    if pd.isna(current_file_data.loc[zeile, 'udpLen']):
                        daten[index] += (current_file_data.loc[zeile, 'tcpLen'])
                    else:
                        daten[index] += current_file_data.loc[zeile, 'udpLen']
    for index, _ in enumerate(os.listdir(dateipfad)):
        daten[index] = daten[index]/actzeitslot

    # Liste mit Indexing für plotten-aufruf
    daten_anzahl = np.arange(zaehler)

    plt.bar(daten_anzahl, daten)
    plt.xlabel('Nummer der Datei')
    plt.ylabel('Durchschnittliche Downloadrate (ermittelt durch Paketgroßen)')


    plt.show()

# ÄNDERUNG: Um den Upload zu bekommen, muss immer das betrachtet werden, was raus geht, also ggf. wo die srcIP == meine IP ist
# Noch ist es ein Downloadraten Berechner
def plotueberordner_uploadrate (dateipfad):

    zaehler = 0
    # zählt wie viele Datein in dem Ordner vorhanden sind
    for filename in os.listdir(dateipfad):
        zaehler += 1

    # initialisierung der  Liste für Performance
    daten = [0] * zaehler

    actzeitslot = 0

    # Befüllung der Liste mit Daten
    # sorted() sortiert nicht wie gewünscht. Es sortiert die Zahlen nicht nach Größe
    for index, filename in enumerate(sorted(os.listdir(dateipfad))):
        full_path = os.path.join(dateipfad, filename, 'all_network_traffic.csv')
        current_file_data = pd.read_csv(full_path)
        actzeit = math.floor(current_file_data.loc[index, 'timestamp'])
        for index1, row in current_file_data.iterrows():
            zeile = index1
            if current_file_data.loc[zeile, 'ipSrc'] == '10.10.0.140':
                if actzeit == math.floor(current_file_data.loc[zeile, 'timestamp']):
                    if pd.isna(current_file_data.loc[zeile, 'udpLen']):
                        daten[index] += (current_file_data.loc[zeile, 'tcpLen'])
                    else:
                        daten[index] += current_file_data.loc[zeile, 'udpLen']

                else:
                    actzeit = math.floor(current_file_data.loc[zeile, 'timestamp'])
                    actzeitslot += 1
                    if pd.isna(current_file_data.loc[zeile, 'udpLen']):
                        daten[index] += (current_file_data.loc[zeile, 'tcpLen'])
                    else:
                        daten[index] += current_file_data.loc[zeile, 'udpLen']
    for index, _ in enumerate(os.listdir(dateipfad)):
        daten[index] = daten[index]/actzeitslot

    # Liste mit Indexing für plotten-aufruf
    daten_anzahl = np.arange(zaehler)

    plt.bar(daten_anzahl, daten)
    plt.xlabel('Nummer der Datei')
    plt.ylabel('Durchschnittliche Downloadrate (ermittelt durch Paketgroßen)')


    plt.show()