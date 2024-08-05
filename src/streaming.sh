#!/bin/bash

# Pfad zur .pcap-Datei
PCAP_FILE="versuch1.pcap"
# Pfad zur Ausgabedatei für die CPU-Überwachung
OUTPUT_FILE="cpu_usage.log"

# Starte tcpreplay und erhalte die PID des Prozesses
tcpreplay -i eno1 $PCAP_FILE &
TCPREPLAY_PID=$!

# Starte die Zeitmessung
START_TIME=$(date +%s)

# Leere die Ausgabedatei und füge eine Kopfzeile hinzu
echo "Zeit (Sekunden), CPU (%)" > $OUTPUT_FILE

# Schleife zur Überwachung der CPU-Auslastung
while ps -p $TCPREPLAY_PID > /dev/null; do
  # Aktuelle CPU-Auslastung in Prozent (gesamtsystemweit)
  CPU_USAGE=$(ps -p $TCPREPLAY_PID -o %cpu --no-headers)

  # Berechne die vergangene Zeit
  CURRENT_TIME=$(date +%s)
  ELAPSED_TIME=$((CURRENT_TIME - START_TIME))

  # Schreibe die Zeit und CPU-Auslastung in die Ausgabedatei
  echo "$ELAPSED_TIME, $CPU_USAGE" >> $OUTPUT_FILE

  # Warte 1 Sekunde
  sleep 1
done

# Script-Ende
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
echo "Wiedergabe abgeschlossen. Gesamtzeit: $TOTAL_TIME Sekunden."
