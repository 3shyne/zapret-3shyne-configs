import sys
import os
import time
import random
from scapy.all import *
from scapy.layers.tls.all import *

def process_file(input_path):
    # load the binary file containing tls data
    try:
        with open(input_path, "rb") as f:
            raw_data = f.read()
    except exception as e:
        print(f"error reading file: {e}")
        return

    tls_pkt = tls(raw_data)

    # check if this is actually a clienthello we can modify
    if tls_pkt.haslayer(tlsclienthello):
        ch = tls_pkt[tlsclienthello]
        
        # grease values help us blend in with normal noise
        grease_types = [0x0a0a, 0x1a1a, 0x2a2a, 0x3a3a, 0x4a4a, 0x5a5a, 0x6a6a, 0x7a7a]
        
        # add a bunch of fake extensions to muddy the waters
        count = 25
        for i in range(count):
            ext_type = random.choice(grease_types) + random.randint(1, 255)
            junk_len = random.randint(16, 128)
            junk_val = os.urandom(junk_len)
            
            new_ext = tls_ext_unknown(type=ext_type, val=junk_val)
            ch.ext.append(new_ext)

        # throw in heavy padding to mess with size-based detection
        padding_ext = tls_ext_padding(padding=b"\x00" * random.randint(400, 800))
        ch.ext.append(padding_ext)

        # shuffle everything so the order doesn't give us away
        random.shuffle(ch.ext)

        # rebuild the packet and save it
        modified_bytes = bytes(tls_pkt)
        
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_modified{ext}"
        
        with open(output_path, "wb") as f:
            f.write(modified_bytes)
            
        print(f"added {count} junk extensions plus padding")
        print(f"saved to: {output_path}")
    else:
        print("error: no valid tls clienthello found in this file")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: drag and drop a .bin file onto this script")
        input("press enter to exit...")
    else:
        process_file(sys.argv[1])
        print("\ndone!")
        time.sleep(3)