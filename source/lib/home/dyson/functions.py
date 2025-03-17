__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"


from iso639 import Lang
from libpurecoollink.dyson import DysonAccount
from libdyson.cloud import DysonAccount
from libdyson.cloud.account import DysonAccountCN
from libdyson.exceptions import DysonOTPTooFrequently
import time
from libdyson.discovery import DysonDiscovery
import libdyson

# Log to Dyson account
# Language is a two characters code (eg: FR)
language = Lang("English")

email = "davewd@me.com"
password = "YOU KNOW WHAT TO DO!"

print("Please choose your account region")
print("1: Mainland China")
print("2: Rest of the World")
region = 2

if region == "1":
    account = DysonAccountCN()
    mobile = input("Phone number: ")
    verify = account.login_mobile_otp(f"+86{mobile}")
    otp = input("Verification code: ")
    verify(otp)
elif region == "2":
    region = "GB"
    account = DysonAccount()
    verify = account.login_email_otp(email, region)

    otp = "GET FROM EMAIL"

    verify(otp, password)
else:
    print(f"Invalid input {region}")
    exit(1)


local_discovery = DysonDiscovery()
local_discovery.start_discovery()
time.sleep(10)
devices = account.devices()
for device in devices:
    print()
    print(f"Serial: {device.serial}")
    print(f"Name: {device.name}")
    print(f"Device Type: {device.product_type}")
    print(f"Credential: {device.credential}")
    device = libdyson.DysonPureHotCoolLink(serial=device.serial, credential=device.credential, device_type=device.product_type)
    DEVICE_IP = local_discovery._discovered[device.serial]
    device.connect(DEVICE_IP)
    print(device._command_topic)

local_discovery.stop_discovery()
