import sys
import os
import time
import random
from scapy.all import *
from scapy.layers.tls.all import *

def process_file(input_path):
    # grab the raw bytes from the input file
    try:
        with open(input_path, "rb") as f:
            raw_data = f.read()
    except exception as e:
        print(f"error reading file: {e}")
        return

    tls_pkt = tls(raw_data)

    # make sure we're actually working with a clienthello
    if tls_pkt.haslayer(tlsclienthello):
        ch = tls_pkt[tlsclienthello]
        
        print(f"obfuscating: {os.path.basename(input_path)}")
        
        # bloat the cipher list with grease and old suites to confuse ja3
        extra_ciphers = [0x1a1a, 0x00ff, 0x003c, 0x003d, 0x5a5a]
        ch.ciphers = extra_ciphers + ch.ciphers

        # dump a ton of junk extensions using grease ranges
        grease_types = [0x0a0a, 0x1a1a, 0x2a2a, 0x3a3a, 0x4a4a, 0x5a5a, 0x6a6a, 0x7a7a]
        for i in range(20):
            ext_type = random.choice(grease_types) + random.randint(1, 100)
            junk_val = os.urandom(random.randint(16, 128))
            ch.ext.append(tls_ext_unknown(type=ext_type, val=junk_val))

        # add variable padding to mess with size-based detection
        ch.ext.append(tls_ext_padding(padding=b"\x00" * random.randint(100, 600)))

        # shuffle everything so nothing stays in expected order
        random.shuffle(ch.ext)

        # enable rare compression methods to trigger deeper inspection
        ch.comp = [0, 1]

        # rebuild and save the modified packet
        modified_bytes = bytes(tls_pkt)
        
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_modified{ext}"
        
        with open(output_path, "wb") as f:
            f.write(modified_bytes)
            
        print(f"dpi obfuscation complete")
        print(f"total extensions: {len(ch.ext)}")
        print(f"saved as: {os.path.basename(output_path)}")
    else:
        print("error: no valid tls clienthello found in this file")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: drag and drop a clienthello .bin file onto this script")
        input("press enter to exit...")
    else:
        process_file(sys.argv[1])
        print("\ndone!")
        time.sleep(3)