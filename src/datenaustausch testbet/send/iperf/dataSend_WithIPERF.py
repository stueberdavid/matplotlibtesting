import subprocess
import iperf3


# Filter aktivieren
#subprocess.run(["sudo", "tc", "qdisc", "add", "dev", "eth0", "root", "netem", "loss", "50%"], check=True)

client = iperf3.Client()
client.duration = 20  # Dauer des Tests in Sekunden
client.server_hostname = '10.0.0.2'
client.port = 5201  # Muss mit dem Server-Port übereinstimmen

result = client.run()
if result.error:
    print(f"Fehler: {result.error}")
else:
    print(f"Gesendete Datenrate: {result.sent_Mbps} Mbps")

# Filter deaktivieren
#subprocess.run(["sudo", "tc", "qdisc", "del", "dev", "eth0", "root"], check=True)
