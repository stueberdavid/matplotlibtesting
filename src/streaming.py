import os
from glob import glob
import subprocess


inputpath = '/media/david/c6a80248-7aa3-42ce-b5ea-8ae505d37261'
inputfilenames = "*.pcap"
all_files = [file
             for path, subdir, files in os.walk(inputpath)
             for file in glob(os.path.join(path, inputfilenames))]

for n in all_files:
    subprocess.run(["sudo", "/home/david/datensenden_Python.sh", n])


print("Programm durchgelaufen!")