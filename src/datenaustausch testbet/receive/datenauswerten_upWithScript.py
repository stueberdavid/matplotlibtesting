import os
import time
import subprocess
import psutil
from datetime import datetime

# Variablen setzen
INTERFACE = "enp0s25"
#INTERFACE = "eno1"
CAPTURE_FILE = "/home/david/test.pcap"
LOG_FILE = "/home/david/receiver_resource_usage.csv"
MEINE_IP = "10.0.0.1"

# Entfernen der alten CAPTURE_FILE, falls vorhanden, und Erstellen eines neuen
if os.path.exists(CAPTURE_FILE):
    os.remove(CAPTURE_FILE)  # Alte Datei löschen
with open(CAPTURE_FILE, 'w') as f:
    pass  # Neue Datei erstellen

# Starte Tshark im Hintergrund
tshark_cmd = ["sudo", "tshark", "-i", INTERFACE, "-w", CAPTURE_FILE, "-f", f"src host {MEINE_IP}"]
tshark_process = subprocess.Popen(tshark_cmd)

# Warte, bis Tshark sicher gestartet ist
time.sleep(1)

# Hole die PID des aktuellen Skripts
script_pid = os.getpid()

def get_cpu_usage(pid):
    try:
        # Überprüfen, ob der Prozess existiert
        proc = psutil.Process(pid)

        # Werte aus der Datei /proc/[pid]/stat
        stat_file = f"/proc/{pid}/stat"
        if not os.path.exists(stat_file):
            return 0.0  # Standardwert zurückgeben, wenn die Datei nicht existiert

        with open(stat_file, 'r') as f:
            stat_values = f.read().split()
            utime = int(stat_values[13])
            stime = int(stat_values[14])
            starttime = int(stat_values[21])

        # Jiffies pro Sekunde ermitteln
        hertz = os.sysconf(os.sysconf_names['SC_CLK_TCK'])

        # Verbrauchte Zeit (in Sekunden)
        cpu_time = (utime + stime) / hertz

        # Gesamte Zeit seit dem Systemstart (in Sekunden)
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.read().split()[0])

        # Gesamte Prozesszeit in Sekunden
        total_time = uptime - (starttime / hertz)

        if total_time <= 0:
            return 0.0

        # CPU-Auslastung in Prozent
        cpu_usage_percentage = (cpu_time / total_time) * 100
        return round(cpu_usage_percentage, 30)

    except Exception as e:
        print(f"Fehler bei der Berechnung der CPU-Auslastung: {e}")
        return 0.0

# Starte die Überwachung der Ressourcennutzung für das Skript
with open(LOG_FILE, 'w') as log_file:
    log_file.write("Zeit;CPU(%);MEM(KB)\n")  # CSV-Header

    try:
        while True:
            proc = psutil.Process(script_pid)
            cpu_usage = get_cpu_usage(script_pid)  # PID des Skripts verwenden
            memory_usage = proc.memory_info().rss / 1024  # Speicher in KB

            log_file.write(f"{datetime.now().strftime('%H:%M:%S')};{cpu_usage:.30f};{memory_usage:.2f}\n")
            log_file.flush()  # Schreibe die Datei sofort auf die Festplatte

            time.sleep(1)

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print("Skriptprozess beendet.")
    except KeyboardInterrupt:
        print("Überwachung abgebrochen.")

# Beende Tshark
print("Beende Tshark...")
tshark_process.terminate()

# Zeige den Inhalt der Logdatei in der Konsole an
with open(LOG_FILE, 'r') as log_file:
    print(log_file.read())
