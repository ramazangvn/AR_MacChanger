import subprocess
import optparse
import re
from rich import print


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--interface", dest="interface", help="interface seçim parametresi..")
    parse_object.add_option("-m", "--mac", dest="mac_address", help="yeni mac address parametresi..")

    (user_input, arguments) = parse_object.parse_args()

    if user_input.interface and user_input.mac_address:
        return str(user_input.interface), str(user_input.mac_address)
    else:
        error_message()

def change_mac_address(interface, mac_address):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])

def control_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))

    if new_mac:
        return new_mac.group(0)
    else:
        return None

def error_message():
    print("[red bold]HATA:[/red bold] Belirtilen parametreler eksik veya hatalı.")
    print("[blue]Kullanım:[/blue] python ar_mac_changer.py -i <interface> -m <mac_address>")
    exit()



print("\n", "[green]*" * 10, "[italic #f8c471]AR_MacChanger", "[green]*" * 10)
print("-" * 38, "\n\n")
(interface, mac_address) = get_user_input()
old_mac = control_new_mac(interface)

change_mac_address(interface, mac_address)
new_mac = control_new_mac(interface)

if new_mac == mac_address:
    print("[#f9e79f]Success!")
    print("-" * 38)
    print(f"[#d7bde2 italic]Önceki mac adresin: [/]{old_mac}")
    print("-" * 38)
    print(f"[#a9cce3 italic]Yeni mac adresin: [/]{new_mac}")
else:
    error_message()