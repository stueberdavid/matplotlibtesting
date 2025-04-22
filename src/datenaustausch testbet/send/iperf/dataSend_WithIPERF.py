import subprocess
from time import sleep
import iperf3
import numpy as np

subprocess.Popen(["sudo","python3", r"/home/david/PycharmProjects/matplotlibtesting/src/datenaustausch testbet/receive/scriptStarter.py"],
                 stdout=subprocess.DEVNULL,
                 stderr=subprocess.DEVNULL)



def generate(bandwidth):
    client = iperf3.Client()
    client.duration = 60  # Dauer des Tests in Sekunden
    client.server_hostname = '10.0.0.1'
    client.port = 5201  # Muss mit dem Server-Port übereinstimmen
    client.blksize = 1500
    client.protocol = "udp"
    client.bandwidth = bandwidth #in Mbit
    #client.reverse = True
    client.run()
    sleep(2)

n = 20 # n = Anzahl der Durchläufe * 3

# Intervall 1: 10^2 bis 10^3
interval_1 = np.logspace(2, 3, num=n)

# Intervall 2: 10^3 bis 10^4
interval_2 = np.logspace(3, 4, num=n)

# Intervall 3: 10^4 bis 10^5
interval_3 = np.logspace(4, 5, num=n)

# Alle Intervalle kombinieren
x_values= np.concatenate([interval_1, interval_2, interval_3])

x_values *= 100000

#Beginn: 10 Mbits/sec

input_x_values = np.round(x_values).astype(int)


for i, bandwidth in enumerate(input_x_values):
    generate(bandwidth)
    print("Senderate: ", bandwidth/1000000, "Mbits/sec")


subprocess.run(["sudo","pkill", "python"], check=True)
