import time
import os
import struct
from scapy.all import *

load_layer("tls")

def generate_client_hello(target_domain="www.google.com", target_size=681):
    rand_sid = os.urandom(32)
    rand_gmt = int(time.time())
    rand_keyshare = os.urandom(32)

    domain_bytes = target_domain.encode('utf-8')
    sni_val = struct.pack("!HBH", len(domain_bytes) + 3, 0, len(domain_bytes)) + domain_bytes
    extensions_data = [
        (0, sni_val),                                                # SNI
        (23, b""),                                                   # EMS
        (65281, b"\x00"),                                            # Renegotiation
        (10, b"\x00\x0c\x00\x1d\x00\x17\x00\x18\x00\x19\x01\x00\x01\x01"), # Groups
        (11, b"\x01\x00"),                                           # EC Formats
        (35, b""),                                                   # Session Ticket
        (16, b"\x00\x0c\x08http/1.1"),                               # ALPN
        (5, b"\x01\x00\x00\x00\x00"),                                # Status Request
        (34, b"\x00\x08\x04\x03\x04\x01\x05\x03\x05\x01"),           # Delegated Creds
        (18, b""),                                                   # SCT
        (51, b"\x00\x67\x00\x1d\x00\x20" + rand_keyshare + b"\x00"*67), # Key Share
        (43, b"\x08\x03\x04\x03\x03\x03\x02\x03\x01"),               # Supported Versions
        (13, b"\x00\x16\x04\x03\x08\x04\x04\x01\x05\x03\x08\x05\x05\x01\x08\x06\x06\x01\x02\x03\x02\x01\x02\x02"), # SigAlgs
        (45, b"\x01\x01"),                                           # PSK Modes
        (28, b"\x40\x00"),                                           # Record Size Limit
        (27, b"\x01\x00\x02\x00\x03\x00\x00"),                       # Cert Compression
    ]

    # padding
    temp_ext = [TLS_Ext_Unknown(type=t, val=v) for t, v in extensions_data]
    ch_temp = TLSClientHello(version=0x0303, gmt_unix_time=rand_gmt, sid=rand_sid, ext=temp_ext)
    
    # Set ciphers
    ciphers_list = [0x1301, 0x1302, 0x1303, 0xC02B, 0xC02F, 0xC02C, 0xC030, 0xCCA9, 0xCCA8, 0xC013, 0xC014, 0x009C, 0x009D, 0x002F, 0x0035, 0x000A, 0x0016]
    try: ch_temp.ciphers = ciphers_list; ch_temp.comp = [0]
    except: ch_temp.cipher_suites = ciphers_list; ch_temp.compression_methods = [0]
    
    current_size = len(raw(TLS(msg=[ch_temp]) if hasattr(TLS(), 'msg') else TLS(handshakes=[ch_temp])))
    padding_needed = target_size - current_size - 4
    
    if padding_needed < 0:
        print(f"Warning: Domain too long. Current size {current_size} exceeds {target_size}.")
        padding_needed = 0

    extensions_data.append((65037, b"\x00" * padding_needed))
    ext_list = [TLS_Ext_Unknown(type=t, val=v) for t, v in extensions_data]
    
    ch = TLSClientHello(version=0x0303, gmt_unix_time=rand_gmt, sid=rand_sid, ext=ext_list)
    try: ch.ciphers = ciphers_list; ch.comp = [0]
    except: ch.cipher_suites = ciphers_list; ch.compression_methods = [0]

    try: pkt = TLS(msg=[ch])
    except: pkt = TLS(handshakes=[ch])
    
    return raw(pkt)

domain = input("Enter domain (e.g. example.com): ") or "www.google.com"
binary_data = generate_client_hello(domain)

with open("browser_style_clienthello.bin", "wb") as f:
    f.write(binary_data)

print(f"Generated {len(binary_data)} bytes for {domain} with randomized SID/KeyShare.")
