import os
import pandas as pd
import pandasplot
import numpy as np

def plotueberordner (dateipfad):
    for filename in os.listdir('dateipfad für datei-ordner'):
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
    for filename, index in os.listdir(dateipfad):
        daten[index] = (os.stat(filename))

    return (daten, daten_anzahl, 'Datei Größe der Datei', 'Nummer der Datei')



