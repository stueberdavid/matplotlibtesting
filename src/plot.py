import numpy as np
from matplotlib import pyplot as plt

def plotten(daten, anzahl):

    x = anzahl
    y = daten

    plt.bar(x, y)

    plt.title('Datenauswertung von Versuch2.csv')
    plt.xlabel('Pakete über die Zeit')
    plt.ylabel('Größe der eingehenden Pakete')
    plt.grid=True

    plt.show()

# plottendoppel nimmt Datensets an und plottet diese in einer gemeinsamen Graphik, dabei wird der kürzere Datensatz
# mit Nullen verlängert, damit die Datensets gleich lang sind (das ist nötig um den Plot zu ermöglichen)
def plottendoppel(daten, anzahl, daten2, anzahl2):

    if len(anzahl) < len(anzahl2):
        x = anzahl2
        for zelle in range(len(anzahl2) - len(anzahl)):
            daten.append(0)
    else:
        x = anzahl
        for zelle in range(len(anzahl) - len(anzahl2)):
            daten2.append(0)

    y = daten
    w = daten2

    plt.plot(x, y, color='green')
    plt.plot(x, w, color='blue')

    plt.title('Datenauswertung von Versuch2.csv')
    plt.xlabel('Pakete über die Zeit')
    plt.ylabel('Größe der eingehenden Pakete')
    plt.grid=True

    plt.show()

def plt_normal(versuch):

    # Zeile gibt an in welcher Zeile der CSV Datei man sich befindet
    zeile = 0

    # intanzahl ist eine Laufvariable die angibt wie viele Werte in der List 'daten' stehen und speichert diese in der Liste
    # 'anzahl'
    intanzahl = 0

    # daten ist eine Liste die immer die Paketgröße abspeichert, wenn ein Paket empfangen wurde
    daten = []

    # anzahl ist eine Liste mit der Anzahl von der Liste 'daten'
    anzahl = []

    # iteriert über die CSV Datei und speichert die Länge der empfangenen Pakete in der Liste 'daten'
    for index, row in versuch.iterrows():
        if (versuch.loc[zeile, 'ip.dst'] == '172.16.31.14'):
            laenge = versuch.loc[zeile, 'frame.len']

            anzahl.append(intanzahl)
            intanzahl += 1
            daten.append(laenge)

        zeile += 1

    return (daten, anzahl)

def plt_overtime(versuch):
    # Zeile gibt an in welcher Zeile der CSV Datei man sich befindet
    zeile = 0

    # daten ist eine Liste die immer die Paketgröße abspeichert, wenn ein Paket empfangen wurde
    daten = []

    # anzahl ist eine Liste mit der Anzahl von der Liste 'daten'
    zeiten = []

    # iteriert über die CSV Datei und speichert die Länge der empfangenen Pakete in der Liste 'daten'
    for index, row in versuch.iterrows():
        if (versuch.loc[zeile, 'ip.dst'] == '172.16.31.14'):
            laenge = versuch.loc[zeile, 'frame.len']

            zeiten.append(versuch.loc[zeile, 'frame.time_epoch'])
            daten.append(laenge)

        zeile += 1

    return (daten, zeiten)

def plt_paketeprosec(versuch):
    # actzeitslot ist eine Laufvariable die den aktuellen Zeitslot angibt
    actzeitslot = 0

    # daten ist eine Liste die immer die Paketgröße abspeichert, wenn ein Paket empfangen wurde
    paketanzahl = []


    # zeitslot ist eine List in der aktuelle Zeitslot gespeichert ist
    zeitslot = []

    actzeit = versuch.loc[0, 'frame.time_epoch']

    for index, row in versuch.iterrows():
        zeile = index
        if (versuch.loc[zeile, 'ip.dst'] == '172.16.31.14'):
            if (actzeit == versuch.loc[zeile, 'frame.time_epoch']):
                paketanzahl[actzeitslot-1] += 1
            else:
                actzeit = actzeit = versuch.loc[zeile, 'frame.time_epoch']
                actzeitslot += 1
                paketanzahl.append(0)
                zeitslot.append(actzeitslot)

    return(paketanzahl, zeitslot)

def plt_byteprosec(versuch):
    # actzeitslot ist eine Laufvariable die den aktuellen Zeitslot angibt
    actzeitslot = 0

    # daten ist eine Liste die immer die Paketgröße abspeichert, wenn ein Paket empfangen wurde
    byteanzahl = []

    # zeitslot ist eine List in der aktuelle Zeitslot gespeichert ist
    zeitslot = []

    actzeit = versuch.loc[0, 'frame.time_epoch']

    for index, row in versuch.iterrows():
        zeile = index
        if (versuch.loc[zeile, 'ip.dst'] == '172.16.31.14'):
            if (actzeit == versuch.loc[zeile, 'frame.time_epoch']):
                byteanzahl[actzeitslot-1] += versuch.loc[zeile, 'frame.len']
            else:
                actzeit = actzeit = versuch.loc[zeile, 'frame.time_epoch']
                actzeitslot += 1
                byteanzahl.append(0)
                zeitslot.append(actzeitslot)


    return(byteanzahl, zeitslot)

# plt_frametopayload gibt das Verhältis zwischen der Größe des gesamten Paketes und dem Payload über die Zeit an
def plt_frametopayload(versuch):
    # Zeile gibt an in welcher Zeile der CSV Datei man sich befindet
    zeile = 0

    # daten ist eine Liste die immer die Paketgröße abspeichert, wenn ein Paket empfangen wurde
    daten = []

    # anzahl ist eine Liste mit der Anzahl von der Liste 'daten'
    anzahl = []
    headersum = 0
    # iteriert über die CSV Datei und speichert die Länge der empfangenen Pakete in der Liste 'daten'
    for index, row in versuch.iterrows():
        if (versuch.loc[zeile, 'ip.dst'] == '172.16.31.14'):
            laenge = versuch.loc[zeile, 'frame.len']
            header = 0

            if (versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ipv6:icmpv6'or
                    versuch.loc[zeile, 'frame.protocols'] == 'ip:eth:ethertype:ipv6:udp:mdns' or
                    versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ipv6:udp:data' or
                    versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ipv6:udp:dhcpv6' or
                    versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ipv6:udp:mdns'):
                header = 48
            elif (versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:quic:tls' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:quic' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:dns' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:goose:cotp' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:dhcp' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:db-lsp-disc:json' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:data' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:udp:mndp'):
                header = 8
            elif versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ieee802a:data':
                header = 4
            elif versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:lldp':
                header = 23
            elif versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:arp':
                header = 28
            elif (versuch.loc[zeile, 'frame.protocols'] == 'eth:llc:stp' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:llc:cdp'):
                header = 36
            elif (versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:tcp' or
                  versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:tcp:tls'):
                header = 20
            elif versuch.loc[zeile, 'frame.protocols'] == 'eth:ethertype:ip:ssdp':
                header = 42

            anzahl.append(index)
            daten.append(laenge-header)

        zeile += 1

    return (daten, anzahl)

def plt_(versuch):

    # daten ist eine Liste die immer die Paketgröße abspeichert, wenn ein Paket empfangen wurde
    flows = []

    # anzahl ist eine Liste mit der Anzahl von der Liste 'daten'
    flowenum = [[]]

    meine_ip = '172.16.31.14'

    # iteriert über die CSV Datei und speichert die Länge der empfangenen Pakete in der Liste 'daten'
    for index, row in versuch.iterrows():

        if (versuch.loc[index, 'ip.dst'] == meine_ip):
            if not versuch.loc[index, 'ip.src'] in flows:
                x = 0
                flowenum.append(versuch.loc[index, 'ip.src'], x)
            else:
                flowenum[versuch.loc[index, 'ip.src'], x] = flowenum[(versuch.loc[index, 'ip.src'], x + 1)]

        if (versuch.loc[index, 'ip.src'] == meine_ip):
            if not versuch.loc[index, 'ip.dst'] in flows:
                x = 0
                flowenum.append(versuch.loc[index, 'ip.dst'], x)
            else:
                flowenum[versuch.loc[index, 'ip.dst'], x] = flowenum[(versuch.loc[index, 'ip.dst'], x + 1)]




    return (flowenum[[]], flows)


