from scapy.all import rdpcap
import pandas as pd

# PCAP-Datei laden
packets = rdpcap("/home/david/PycharmProjects/matplotlibtesting/src/Testergebnisse/Ergebnis 1 - Download/test.pcap")

# Zeitstempel extrahieren
timestamps = [packet.time for packet in packets]

# Timestamps in Sekunden runden und zählen
df = pd.DataFrame(timestamps, columns=['timestamp'])
df['second'] = df['timestamp'].astype(int)  # Zeitstempel in Sekunden runden
packet_counts = df['second'].value_counts().sort_index()  # Pakete pro Sekunde zählen

# In DataFrame umwandeln für bessere Darstellung
result_df = packet_counts.reset_index()
result_df.columns = ['second', 'packet_count']

# Optional: Ergebnis speichern
result_df.to_csv('packet_counts_per_second.csv', index=False)

# Ausgabe anzeigen
print(result_df.head())

