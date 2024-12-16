import os
import time
import subprocess
import psutil

# Variablen setzen
INTERFACE = "enp0s25"
#INTERFACE = "eno1"
CAPTURE_FILE = "/home/david/test.pcap"
LOG_FILE = "/home/david/receiver_resource_usage.csv"

# Entfernen der alten CAPTURE_FILE, falls vorhanden, und Erstellen eines neuen
if os.path.exists(CAPTURE_FILE):
    os.remove(CAPTURE_FILE)  # Alte Datei löschen
with open(CAPTURE_FILE, 'w') as f:
    pass  # Neue Datei erstellen

# Starte Tshark im Hintergrund (hier ohne Filter, Filter kann hinzugefügt werden)
tshark_cmd = ["sudo", "tshark", "-i", INTERFACE, "-w", CAPTURE_FILE]
tshark_process = subprocess.Popen(tshark_cmd)

# Warte, bis Dumpcap sicher gestartet ist
time.sleep(1)

# Suche nach der PID von Dumpcap (das von Tshark aufgerufen wird)
dumpcap_pid = None
for proc in psutil.process_iter(['pid', 'name']):
    if 'dumpcap' in proc.info['name']:
        dumpcap_pid = proc.info['pid']
        break

if dumpcap_pid is None:
    print("Dumpcap-Prozess nicht gefunden.")
    tshark_process.terminate()
    exit(1)


def get_cpu_usage(pid):
    try:
        # Überprüfen, ob der Prozess existiert
        proc = psutil.Process(pid)

        # Öffne die Datei /proc/[pid]/stat
        stat_file = f"/proc/{pid}/stat"
        if not os.path.exists(stat_file):
            print(f"Datei {stat_file} existiert nicht.")
            return 0.0  # Standardwert zurückgeben, wenn die Datei nicht existiert

        # Werte aus der Datei extrahieren
        with open(stat_file, 'r') as f:
            stat_values = f.read().split()
            utime = int(stat_values[13])  # 14. Wert (Index 13 in Python)
            stime = int(stat_values[14])  # 15. Wert (Index 14 in Python)
            starttime = int(stat_values[21])  # 22. Wert (Index 21 in Python)

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
            return 999.0  # Standardwert zurückgeben

        # CPU-Auslastung in Prozent
        cpu_usage_percentage = (cpu_time / total_time) * 100
        return round(cpu_usage_percentage, 15)

    except Exception as e:
        print(f"Fehler bei der Berechnung der CPU-Auslastung: {e}")
        return 0.0  # Standardwert zurückgeben


# Starte die Überwachung der Ressourcennutzung für Dumpcap
with open(LOG_FILE, 'w') as log_file:
    log_file.write("Time in Milliseconds since Epoche;CPU(%);MEM(KB)\n")  # CSV-Header

    # Starte die Überwachung in einer Schleife
    try:
        while True:
            proc = psutil.Process(dumpcap_pid)
            cpu_usage = get_cpu_usage(dumpcap_pid)  # PID übergeben
            memory_usage = proc.memory_info().rss / 1024  # Speicher in KB

            # Schreibe die Ressourcennutzung in die CSV-Datei mit 6 Nachkommastellen für CPU
            log_file.write(f"{time.time_ns()};{cpu_usage:.15f};{memory_usage:.2f}\n")
            log_file.flush()  # Schreibe die Datei sofort auf die Festplatte

            time.sleep(1)

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print("Dumpcap-Prozess beendet.")
    except KeyboardInterrupt:
        print("Überwachung abgebrochen.")

# Beende Tshark und Dumpcap
print("Beende Tshark und Dumpcap...")
tshark_process.terminate()
try:
    proc.terminate()  # Dumpcap-Prozess terminieren
    time.sleep(1)
    if psutil.pid_exists(dumpcap_pid):
        proc.kill()  # Falls noch aktiv, endgültig beenden
except psutil.NoSuchProcess:
    print("Dumpcap bereits beendet.")

# Zeige den Inhalt der Logdatei in der Konsole an
with open(LOG_FILE, 'r') as log_file:
    print(log_file.read())