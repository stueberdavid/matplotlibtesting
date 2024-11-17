import os
import subprocess
import time
import psutil # Für die Ressourcennutzung
from glob import glob

def monitor_resource_usage(pid, log_file):
    # CPU Auslastung monitoren und in die LOG-Datei schreiben
    with open(log_file, 'w') as f:
        f.write("Zeit CPU(%) MEM(KB)\n")
        try:
            while psutil.pid_exists(pid):
                # Hole den Prozess und die Ressourcennutzung
                p = psutil.Process(pid)
                cpu_usage = p.cpu_percent(interval=1)  # CPU-Nutzung in Prozent
                memory_usage = p.memory_info().rss / 1024  # Arbeitsspeicher in KB

                # Zeitstempel hinzufügen
                timestamp = time.strftime("%H:%M:%S")
                f.write(f"{timestamp} {cpu_usage} {memory_usage}\n")
                f.flush()
                time.sleep(1)
        except psutil.NoSuchProcess:
            pass

def send_pcap(interface, pcap_file, log_file):
    # Senden der Dateien und gleichzeitige CPU-Überwachung

    tcpreplay_cmd = ["sudo", "tcpreplay", f"--intf1={interface}", pcap_file]
    process = subprocess.Popen(tcpreplay_cmd)

    # Überwache die Ressourcennutzung in einem separaten Thread
    monitor_resource_usage(process.pid, log_file)

    # Warte, bis der tcpreplay-Prozess fertig ist
    process.wait()

# Verzeichnispfad und Dateinamenmuster
inputpath = '/media/david/c6a80248-7aa3-42ce-b5ea-8ae505d37261'

inputfilenames = "*.pcap"
log_file = "../../sender_resource_usage.log"
interface = "enp0s25"  # Netzwerk-Schnittstelle

# Finde alle PCAP-Dateien im Verzeichnis
all_files = [file
             for path, subdir, files in os.walk(inputpath)
             for file in glob(os.path.join(path, inputfilenames))]

# Sende jede PCAP-Datei
for pcap_file in all_files:
    send_pcap(interface, pcap_file, log_file)
    time.sleep(20)  # Pause zwischen den Übertragungen
