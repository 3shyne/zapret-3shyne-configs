import sys
import os
import time
import random
from scapy.all import *
from scapy.layers.tls.all import *

def process_file(input_path):
    # read the raw tls data from disk
    try:
        with open(input_path, "rb") as f:
            raw_data = f.read()
    except exception as e:
        print(f"error reading file: {e}")
        return

    tls_pkt = tls(raw_data)

    # only proceed if we actually have a clienthello to work with
    if tls_pkt.haslayer(tlsclienthello):
        ch = tls_pkt[tlsclienthello]

        # grease values make our junk look more natural
        grease_types = [0x0a0a, 0x1a1a, 0x2a2a, 0x3a3a, 0x4a4a, 0x5a5a, 0x6a6a, 0x7a7a]

        # add just enough noise to avoid fingerprinting
        count = 12
        for i in range(count):
            ext_type = random.choice(grease_types) + random.randint(1, 255)
            junk_len = random.randint(8, 64)
            junk_val = os.urandom(junk_len)

            new_ext = tls_ext_unknown(type=ext_type, val=junk_val)
            ch.ext.append(new_ext)

        # light padding to avoid looking too sparse
        padding_ext = tls_ext_padding(padding=b"\x00" * random.randint(200, 400))
        ch.ext.append(padding_ext)

        # randomize extension order to break pattern matching
        random.shuffle(ch.ext)

        # write the modified packet back to disk
        modified_bytes = bytes(tls_pkt)

        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_modified{ext}"

        with open(output_path, "wb") as f:
            f.write(modified_bytes)

        print(f"added {count} lightweight junk extensions plus padding")
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