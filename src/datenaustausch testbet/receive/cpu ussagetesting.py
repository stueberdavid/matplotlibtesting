import os
import time
import subprocess
import psutil

LOG_FILE = "/home/david/receiver_resource_usage.csv"

# Starte Tshark im Hintergrund (hier ohne Filter, Filter kann hinzugefügt werden)
tshark_cmd = ["sudo", "wireshark"]
tshark_process = subprocess.Popen(tshark_cmd)

# Warte, bis Dumpcap sicher gestartet ist
time.sleep(1)

# Suche nach der PID von Dumpcap (das von Tshark aufgerufen wird)
wireshark_pid = None
for proc in psutil.process_iter(['pid', 'name']):
    if 'wireshark' in proc.info['name']:
        wireshark_pid = proc.info['pid']
        break

if wireshark_pid is None:
    print("Dumpcap-Prozess nicht gefunden.")
    tshark_process.terminate()
    exit(1)


def get_cpu_usage(pid):
    last_idle = last_total = 0
    while True:
        with open(f'/proc/{pid}/stat') as f:
            fields = [float(column) for column in f.readline().strip().split()[1:]]
        idle, total = fields[3], sum(fields)
        idle_delta, total_delta = idle - last_idle, total - last_total
        last_idle, last_total = idle, total
        utilisation = 100.0 * (1.0 - idle_delta / total_delta)
        print('%5.1f%%' % utilisation, end='\r')
        time.sleep(5)


# Starte die Überwachung der Ressourcennutzung für Dumpcap
with open(LOG_FILE, 'w') as log_file:
    log_file.write("Time in Milliseconds since Epoche;CPU(%);MEM(KB)\n")  # CSV-Header

    # Starte die Überwachung in einer Schleife
    try:
        while True:
            proc = psutil.Process(wireshark_pid)
            cpu_usage = get_cpu_usage(wireshark_pid)  # PID übergeben
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
    if psutil.pid_exists(wireshark_pid):
        proc.kill()  # Falls noch aktiv, endgültig beenden
except psutil.NoSuchProcess:
    print("Dumpcap bereits beendet.")

# Zeige den Inhalt der Logdatei in der Konsole an
with open(LOG_FILE, 'r') as log_file:
    print(log_file.read())