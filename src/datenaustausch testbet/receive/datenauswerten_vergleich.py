import os
import time
import subprocess
import psutil
from datetime import datetime


# -------------------IN BEARBEITUNG-------------------
#-----------------------------------------------------

# Funktion zur Überwachung des Netzwerkverkehrs mit Filter und Ressourcennutzung
def monitor_traffic(interface, capture_file, log_file, filter_expr=None):
    # Entfernen der alten CAPTURE_FILE, falls vorhanden, und Erstellen eines neuen
    if os.path.exists(capture_file):
        os.remove(capture_file)  # Alte Datei löschen
    with open(capture_file, 'w') as f:
        pass  # Neue Datei erstellen

    # Starte Tshark im Hintergrund mit dem übergebenen Filter
    tshark_cmd = ["sudo", "tshark", "-i", interface, "-w", capture_file]
    if filter_expr:
        tshark_cmd.extend(["-f", filter_expr])  # Filter hinzufügen, falls vorhanden

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
        return

    # Funktion zur Berechnung der CPU-Auslastung
    def get_cpu_usage(proc):
        try:
            return proc.cpu_percent(interval=1) / psutil.cpu_count()
        except psutil.NoSuchProcess:
            return None

    # Starte die Überwachung der Ressourcennutzung für Dumpcap
    with open(log_file, 'w') as log_file:
        log_file.write("Zeit;CPU(%);MEM(KB)\n")  # CSV-Header

        # Starte die Überwachung in einer Schleife
        try:
            while True:
                proc = psutil.Process(dumpcap_pid)
                cpu_usage = get_cpu_usage(proc)
                memory_usage = proc.memory_info().rss / 1024  # Speicher in KB

                # Schreibe die Ressourcennutzung in die CSV-Datei
                log_file.write(f"{datetime.now().strftime('%H:%M:%S')};{cpu_usage:.2f};{memory_usage:.2f}\n")
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
    with open(log_file, 'r') as log_file:
        print(log_file.read())


# Parameter definieren
interface = "enp0s25"
capture_file = "/home/david/test.pcap"
log_file = "/home/david/receiver_resource_usage.csv"
filter_expr = "tcp port 80"  # Beispiel für einen Filter, hier HTTP-Traffic


monitor_traffic(interface, capture_file, log_file, filter_expr)
