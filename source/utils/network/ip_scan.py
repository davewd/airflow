__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import subprocess
import os


def all_local_ips():
    devices = []
    for device in os.popen("arp -a"):
        devices.append(device)
        print(device)


def ip_for_mac_address(mac_address):
    cmd = f'arp -a | findstr "{mac_address}" '
    returned_output = subprocess.check_output((cmd), shell=True, stderr=subprocess.STDOUT)
    print(returned_output)
    parse = str(returned_output).split(" ", 1)
    ip = parse[1].split(" ")
    print(ip[1])


def main() -> None:
    all_local_ips()
    mac_address = "C8-FF-77-DB-5A-29"
    ip_for_mac_address(mac_address)


if __name__ == "__main__":
    main()
