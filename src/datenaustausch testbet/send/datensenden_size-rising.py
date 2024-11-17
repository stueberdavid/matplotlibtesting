import os
import subprocess
import re
import time

PKTGEN_PATH: str = "/proc/net/pktgen"
STARTS_WITH_KPKTGEND: re.Pattern = re.compile(r"^kpktgend_\d*$")
INTERFACE = "enp0s25"


# Funktion, um in das Pktgen-System zu schreiben
def write_pktgen(filepath: str, command: str) -> None:
    with open(os.path.join(PKTGEN_PATH, filepath), "w") as file:
        subprocess.run(["echo", command], stdout=file)


# Funktion, um Pktgen zu initialisieren
def setup() -> None:
    subprocess.run(["modprobe", "pktgen"])


# Funktion zur Bereinigung von Geräten
def cleanup() -> None:
    for file in filter(STARTS_WITH_KPKTGEND.match, os.listdir(PKTGEN_PATH)):
        write_pktgen(file, "rem_device_all")


# Funktion zur Generierung von Paketen
def generate(mac_dst: str, ip_src: str, ip_dst: str, udp_src: int, udp_dst: int, packetcount: int, packetrate: str,
             interface: str = INTERFACE, core: int = 0, size: int = 1514) -> None:
    write_pktgen(f"kpktgend_{core}", f"add_device {interface}@{core}")
    write_pktgen(f"{interface}@{core}", f"dst_mac {mac_dst}")
    write_pktgen(f"{interface}@{core}", f"dst_min {ip_dst}")
    write_pktgen(f"{interface}@{core}", f"dst_max {ip_dst}")
    write_pktgen(f"{interface}@{core}", f"src_min {ip_src}")
    write_pktgen(f"{interface}@{core}", f"src_max {ip_src}")
    write_pktgen(f"{interface}@{core}", f"udp_src_min {udp_src}")
    write_pktgen(f"{interface}@{core}", f"udp_src_max {udp_src}")
    write_pktgen(f"{interface}@{core}", f"udp_dst_min {udp_dst}")
    write_pktgen(f"{interface}@{core}", f"udp_dst_max {udp_dst}")
    write_pktgen(f"{interface}@{core}", f"pkt_size {size}")
    write_pktgen(f"{interface}@{core}", f"rate {packetrate}")
    write_pktgen(f"{interface}@{core}", f"count {packetcount}")
    write_pktgen("pgctrl", "start")
    cleanup()


# Hauptfunktion zur Durchführung von 10 Durchläufen
def run_tests() -> None:
    mac_dst = "84:69:93:0c:59:45"
    ip_src = "10.0.0.2"
    ip_dst = "10.0.0.1"
    udp_src = 50000
    udp_dst = 50000
    size = 1500  # Paketgröße in Bytes
    initial_rate = 1000  # Anfangsrate in Paketen pro Sekunde
    duration = 20  # Dauer des Sendens in Sekunden

    for i in range(10):
        rate = initial_rate * (i + 1)  # Erhöhe die Rate pro Iteration
        packetcount = rate * duration  # Berechne die Anzahl der Pakete für 20 Sekunden

        print(f"Run {i + 1}: Sending {packetcount} packets at a rate of {rate} pkts/sec for 20 seconds.")

        # Pakete generieren
        generate(
            mac_dst,
            ip_src,
            ip_dst,
            udp_src,
            udp_dst,
            packetcount,
            f"{rate}pps",  # Rate in Paketen pro Sekunde
            size=size
        )

        # Warte 2 Sekunden nach jedem Durchlauf
        time.sleep(2)


# Setup und Cleanup aufrufen, um sicherzustellen, dass alles vorbereitet ist
setup()
cleanup()
run_tests()
