import sys
import os
import time
import argparse
from scapy.all import sniff, conf
from scapy.layers.tls.all import tls, tlsclienthello

# set up command line arguments for filename customization
parser = argparse.ArgumentParser(description="capture tls clienthello and save to .bin")
parser.add_argument("-name", "-n", type=str, help="filename to save (e.g., ozon)", default="client_hello")
args = parser.parse_args()

# make sure the output file has a .bin extension
filename = args.name if args.name.endswith(".bin") else f"{args.name}.bin"

# pick the network interface we'll listen on (index 9 is usually wi-fi/ethernet)
target_index = 9
try:
    target_iface = conf.ifaces.dev_from_index(target_index)
except exception:
    print(f"error: no interface found at index {target_index}")
    print("try checking available interfaces with 'scapy' then 'conf.ifaces'")
    sys.exit(1)

def save_client_hello(pkt):
    # look for tls clienthello packets in the stream
    if pkt.haslayer(tlsclienthello):
        # grab just the tls layer bytes (strips away ip/tcp headers)
        tls_data = bytes(pkt[tls])
        
        with open(filename, "wb") as f:
            f.write(tls_data)
            
        print(f"\ncaptured clienthello ({len(tls_data)} bytes)")
        print(f"saved to: {filename}")
        sys.exit(0)

print(f"sniffing on: {target_iface.description} (interface index {target_index})")
print(f"saving to: {filename}")
print("waiting for tls traffic on port 443...")
print("tip: open a browser tab or run 'curl https://www.ozon.ru' to trigger capture")

# start listening for tls handshakes
try:
    sniff(iface=target_iface, filter="tcp port 443", prn=save_client_hello, store=0)
except keyboardinterrupt:
    print("\ncapture aborted by user")
    sys.exit(0)
except exception as e:
    print(f"\nerror during capture: {e}")
    sys.exit(1)