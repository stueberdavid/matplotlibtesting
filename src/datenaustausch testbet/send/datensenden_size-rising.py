import os
import subprocess
import re
import argparse

from fontTools.misc.cython import returns

PKTGEN_PATH: str = "/proc/net/pktgen"
STARTS_WITH_KPKTGEND: re.Pattern = re.compile(r"^kpktgend_\d*$")
INTERFACE = "enp0s25"

def write_pktgen(filepath: str, command: str) -> None:
    with open(os.path.join(PKTGEN_PATH, filepath), "w") as file:
        subprocess.run(["echo", command], stdout=file)

def setup() -> None:
    subprocess.run(["modprobe", "pktgen"])

def cleanup() -> None:
    for file in filter(STARTS_WITH_KPKTGEND.match, os.listdir(PKTGEN_PATH)):
        write_pktgen(file, "rem_device_all")

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




def main(rate: str) -> None:
    setup()
    cleanup()

    generate(
        "84:69:93:0c:59:45",   # Beispiel-MAC-Adresse
        "10.0.0.2",            # Beispiel-Quell-IP
        "10.0.0.1",            # Beispiel-Ziel-IP
        50000,                 # Beispiel-UDP-Quellport
        50000,                 # Beispiel-UDP-Zielport
        50000000000,           # Beispiel-Paketanzahl
        rate,                  # Rate aus Kommandozeilen-Argument
        size=1500
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Netzwerkpaket-Generator mit variabler Rate.")
    parser.add_argument("rate", type=str, help="Die Datenrate in Bit pro Sekunde.")
    args = parser.parse_args()
    main(args.rate)
