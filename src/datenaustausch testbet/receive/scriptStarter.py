import subprocess
import signal
import sys
import os

# Prozesse speichern
processes = []

def start_script(script_path):
    try:
        process = subprocess.Popen(
            ["sudo", "python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Setzt eine neue Sitzungs-ID, damit wir alle Prozesse beenden können
        )
        processes.append(process)
        print(f"Gestartet: {script_path} (PID: {process.pid})")
    except Exception as e:
        print(f"Fehler beim Starten von {script_path}: {e}")

def stop_scripts():
    """Beendet alle gestarteten Skripte."""
    print("Beende alle gestarteten Skripte...")
    for process in processes:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print(f"Beendet: PID {process.pid}")
        except Exception as e:
            print(f"Fehler beim Beenden von PID {process.pid}: {e}")

def signal_handler(sig, frame):
    """Signal-Handler für SIGINT/SIGTERM."""
    print("\nSignal empfangen. Skript wird beendet...")
    stop_scripts()
    sys.exit(0)

if __name__ == "__main__":
    # Signal-Handler registrieren
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Pfade zu den Skripten
    all = "/home/david/PycharmProjects/matplotlibtesting/src/datenaustausch testbet/receive/datenauswerten_all.py"
    down = "/home/david/PycharmProjects/matplotlibtesting/src/datenaustausch testbet/receive/datenauswerten_down.py"
    up = "/home/david/PycharmProjects/matplotlibtesting/src/datenaustausch testbet/receive/datenauswerten_up.py"

    # Skripte starten
    start_script(all)
    start_script(down)
    start_script(up)

    # Warten, bis der Benutzer das Skript beendet
    try:
        while True:
            pass
    except KeyboardInterrupt:
        signal_handler(None, None)
