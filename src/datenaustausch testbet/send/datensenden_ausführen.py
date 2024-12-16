import subprocess
import time
from asyncio import timeout
from time import sleep

# Liste der Raten, die verwendet werden sollen
raten = ["100000000", "200000000", "500000000"]  # in Bit pro Sekunde

# Dauer für jedes Skript (in Sekunden)
dauer = 20

def run_script(rate: str):
    # Befehl zum Aufrufen des empfangenden Skripts mit der Rate
    command = ["python3", "/home/david/PycharmProjects/matplotlibtesting/src/datenaustausch testbet/send/datensenden_size-rising.py", rate]

    try:
        subprocess.run(command, timeout=10)  # Beendet nach 10 Sekunden


    except subprocess.TimeoutExpired:
        print("Das Programm wurde nach 10 Sekunden beendet.")



def main():
    for rate in raten:
        print(f"Starte Skript mit Rate {rate} Bit/s...")
        run_script(rate)

if __name__ == "__main__":
    main()
