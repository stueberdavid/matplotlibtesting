import subprocess
from time import sleep
import iperf3
import numpy as np

subprocess.Popen(["sudo","python3", r"/home/david/PycharmProjects/matplotlibtesting/src/datenaustausch testbet/receive/scriptStarter.py"],
                 stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL)



def generate(bandwidth):
    client = iperf3.Client()
    client.duration = 7  # Dauer des Tests in Sekunden
    client.server_hostname = '10.0.0.1'
    client.port = 5201  # Muss mit dem Server-Port übereinstimmen
    client.blksize = 1500
    client.protocol = "udp"
    client.bandwidth = bandwidth
    client.run()
    sleep(2)

# Beispiel: Werte von 1 bis 1000 logarithmisch verteilen
x_values = np.logspace(0, 3, num=15)*100000  # 10^0 = 1 bis 10^3 = 1000
input_x_values = np.round(x_values).astype(int)

for i, bandwidth in enumerate(input_x_values):
    generate(bandwidth)
    print("Senderate: ", bandwidth/1000000, "Mbits/sec")


subprocess.run(["sudo","pkill", "python"], check=True)
