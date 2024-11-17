import iperf3

iperf_server = iperf3.Server()
iperf_server.port = 5201

while True:
    result = iperf_server.run()