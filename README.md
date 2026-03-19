# 🛡️ Simple DDoS Lab Guide — Metasploitable VM + Wireshark Analysis

> **A Practical, Hands-On Lab for Learning DDoS Attack Mechanics**  
> **Tools Used:** Python · Scapy · Wireshark · Metasploitable VM · VirtualBox

---

## ⚠️ Important — Read This First

This lab is **strictly for educational purposes**. All attacks are performed in an **isolated virtual environment** using Metasploitable — a deliberately vulnerable Linux VM designed for security training.

> **⚠️ WARNING:** Attacking any computer, server, or network you don't own or have explicit permission to test is **illegal** and can result in severe criminal penalties. This lab exists so you can *understand* how DDoS attacks work in a safe, controlled environment — not to misuse this knowledge maliciously.

---

## 🤔 What Is This Lab About?

This lab provides a **safe, isolated environment** to simulate and analyze DDoS (Distributed Denial of Service) attacks. You'll learn by doing — setting up a target VM, launching simulated attacks, and watching the network traffic unfold in real-time using Wireshark.

### Why Use Metasploitable?

Metasploitable is an intentionally vulnerable Linux virtual machine created by Rapid7 for security training and testing. It's the perfect target for this lab because:

- It's **safe and legal** to attack (you own it)
- It has **many open ports and services** by default
- It requires **no additional configuration**
- It's widely used in cybersecurity education

### What You'll Learn

By completing this lab, you will:

- Understand the mechanics of **SYN Flood** and **UDP Flood** attacks
- Learn how to **capture and analyze network traffic** with Wireshark
- Set up a **virtual network lab environment** using VirtualBox
- Recognize DDoS attack signatures in network captures
- Gain hands-on experience with **real-world security tools**

---

## 📦 What You'll Need

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **Host OS** | Windows, macOS, or Linux |
| **VirtualBox** | Version 6.0 or higher ([Download](https://www.virtualbox.org/wiki/Downloads)) |
| **Metasploitable VM** | Available from Rapid7 ([Download](https://information.rapid7.com/download-metasploitable-2017.html)) |
| **Wireshark** | Free network protocol analyzer ([Download](https://www.wireshark.org/download.html)) |
| **Python 3** | Version 3.6 or higher |
| **Scapy** | Python packet manipulation library |

### Python Setup

```bash
# Install Scapy (the packet crafting library)
pip install scapy

# On Linux, if you get permission errors:
pip install scapy --break-system-packages
```

---

## 🧠 Understanding the Attacks

Before running the attacks, let's understand what they do and why they work.

### Attack 1 — SYN Flood

**What it exploits:** The TCP three-way handshake mechanism.

When a client connects to a server, TCP uses a 3-step handshake:

```
Client              Server
   |  ─── SYN ───→     |    "Hello, I want to connect"
   |  ←── SYN-ACK ───  |    "Sure! Ready when you are"
   |  ─── ACK ───→     |    "Confirmed, let's talk!"
        ✅ Connection Established
```

**The Attack:**

```
Attacker (fake IP)     Server
   |  ─── SYN ───→        |    Sends thousands of SYN packets
   |  ←── SYN-ACK ───     |    Server allocates resources & waits
   |      (silence)       |    Attacker never completes handshake
   |      (silence)       |    Server's connection table fills up
                          |    Real users → CONNECTION REFUSED
```

The attacker uses **spoofed (fake) IP addresses**, so the server can never reach them back. The server is left holding thousands of half-open connections, exhausting its resources.

---

### Attack 2 — UDP Flood

**What it exploits:** UDP's connectionless nature and the server's obligation to respond.

UDP (User Datagram Protocol) doesn't require a handshake — data is just sent. When UDP packets arrive at closed ports, the server must respond with ICMP "Port Unreachable" messages.

**The Attack:**

```
Attacker                   Server
   |  ─── UDP packet to port 12345  →   |    Random junk data
   |  ←── ICMP Port Unreachable ────    |    Server responds
   |  ─── UDP packet to port 23456  →   |    Different port
   |  ←── ICMP Port Unreachable ────    |    Server responds again
   |  ─── (repeat thousands of times)   |
   |                                      |    Bandwidth saturated
   |                                      |    CPU overwhelmed
```

This floods the server's bandwidth and forces it to waste CPU cycles processing and responding to junk packets.

---

## 🚀 Easy 5-Step Lab Setup

Follow these steps in order to set up and run your DDoS simulation lab.

---

### Step 1 — Setup VirtualBox Network

Create a Host-Only network so your host machine can communicate with the Metasploitable VM.

1. **Open VirtualBox**
2. Go to: **File → Tools → Network Manager**
3. Click **"Create"** to make a new Host-Only network
   - This creates a virtual network: `192.168.56.x`
4. Select your **Metasploitable VM** → **Settings** → **Network**
5. Set **Adapter 1** to **"Host-Only Adapter"**
6. Select the network you just created (usually `vboxnet0`)
7. Click **OK**, then **Start** the VM

> **💡 What is Host-Only Networking?**  
> It creates a private network between your host and VM. The VM can't reach the internet, but your host can communicate with it directly. Perfect for isolated security labs!

---

### Step 2 — Find Metasploitable IP Address

Once the VM boots, you'll see a login prompt.

1. **Login credentials:**
   - Username: `msfadmin`
   - Password: `msfadmin`

2. **Find the IP address:**
   ```bash
   ip addr show
   ```

3. **Look for a line like:**
   ```
   inet 192.168.56.xxx brd 192.168.56.255 scope global eth0
   ```

4. **Write down this IP address!** You'll need it for the attack scripts.

> **📝 Note:** The IP will typically be `192.168.56.101` or similar (first available address in the Host-Only network).

---

### Step 3 — Start Wireshark Capture

Now let's set up Wireshark to capture all the attack traffic.

1. **Open Wireshark** on your host machine
2. **Select the correct capture interface:**
   - **Windows:** Look for "VirtualBox Host-Only Adapter"
   - **Linux/macOS:** Look for "vboxnet0"
3. Click the **blue shark fin icon** (or double-click the interface) to start capture
4. Leave Wireshark running — you'll see the attack in real-time!

> **🔧 Troubleshooting:** If you don't see the VirtualBox interface in Wireshark:
> - **Linux:** Start Wireshark with `sudo wireshark`
> - **Alternative:** Add your user to the `wireshark` group: `sudo usermod -aG wireshark $USER` (then logout/login)

---

### Step 4 — Run the Attack Scripts

Before running, edit the target IP in your attack scripts.

**Edit the script files:**

```python
# Open the script and change this line:
TARGET_IP = "192.168.56.101"  # ← Change to YOUR Metasploitable IP
```

**Run SYN Flood Attack:**

```bash
# Linux / macOS
sudo python3 simple_syn_flood.py

# Windows (run Command Prompt as Administrator)
python simple_syn_flood.py
```

**Run UDP Flood Attack:**

```bash
# Linux / macOS
sudo python3 simple_udp_flood.py

# Windows (run Command Prompt as Administrator)
python simple_udp_flood.py
```

> **🔐 Why sudo/Administrator?**  
> Crafting and sending raw network packets requires root/admin privileges. This is a security feature of the operating system.

---

### Step 5 — Analyze Traffic in Wireshark

This is where the real learning happens! Let's analyze what you captured.

---

#### 🔵 Analyzing SYN Flood

**In the Wireshark filter bar, type:**

```
tcp.flags.syn == 1
```

**What you'll observe:**

| Observation | Explanation |
|-------------|-------------|
| Many SYN packets to target IP | These are your attack packets |
| All going to port 80 (or chosen port) | The target service being flooded |
| SYN-ACK responses from Metasploitable | Server trying to complete handshakes |
| **NO final ACK responses** | Attack never completes connections |

**Additional filters for deeper analysis:**

```
# Show only initial SYN packets (no ACK flag)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Show only SYN-ACK responses from server
tcp.flags.syn == 1 && tcp.flags.ack == 1

# Filter by your target IP
ip.addr == 192.168.56.101
```

**View statistics:**

- **Statistics → Conversations → TCP tab** — See all TCP "conversations" (mostly incomplete!)
- **Statistics → IO Graph** — Visualize the traffic spike
- **Analyze → Expert Info** — Wireshark flags incomplete handshakes

---

#### 🟠 Analyzing UDP Flood

**In the Wireshark filter bar, type:**

```
udp
```

**What you'll observe:**

| Observation | Explanation |
|-------------|-------------|
| Massive UDP packets to target | Attack traffic blasting random ports |
| Random destination ports | Attacker spraying across all ports |
| ICMP "Port Unreachable" messages | Server responding to closed ports |
| High packets/second rate | Bandwidth consumption in action |

**Additional useful filters:**

```
# Show ICMP port unreachable messages
icmp.type == 3

# Filter all traffic to/from target
ip.addr == 192.168.56.101

# Show UDP traffic only to specific port
udp.dstport == 12345
```

**View statistics:**

- **Statistics → Protocol Hierarchy** — See UDP dominate the traffic
- **Statistics → Conversations → UDP tab** — Identify top talkers
- **Statistics → Packet Lengths** — See distribution of packet sizes

---

## 📊 Quick Reference — Wireshark Filters

| Filter | What It Shows |
|--------|---------------|
| `tcp.flags.syn == 1` | All SYN packets |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Only initial SYN (no ACK) |
| `tcp.flags.syn == 1 && tcp.flags.ack == 1` | SYN-ACK responses from server |
| `udp` | All UDP traffic |
| `icmp.type == 3` | Port unreachable messages |
| `ip.addr == 192.168.56.101` | All traffic to/from target |

---

## 🔧 Troubleshooting Guide

| Problem | Solution |
|---------|----------|
| **Can't see `vboxnet0` in Wireshark** | Start Wireshark with `sudo`, or add user to `wireshark` group |
| **No packets captured** | Ensure VM is running. Test with: `ping 192.168.56.101` |
| **Connection refused errors** | Try different ports: 21 (FTP), 22 (SSH), 139 (SMB), 8080 (HTTP-Alt) |
| **Permission denied when running scripts** | Use `sudo` on Linux/Mac, run as Administrator on Windows |
| **VM won't start** | Ensure VirtualBox Extension Pack is installed |
| **Can't login to Metasploitable** | Default credentials: `msfadmin` / `msfadmin` |
| **IP address not showing** | Make sure Adapter 1 is set to Host-Only, not NAT |

---

## 🛡️ Defense Perspective

Understanding attacks helps you defend against them. Here's how real systems mitigate these threats:

### Against SYN Flood:

- **SYN Cookies:** Server doesn't allocate resources until handshake completes
- **Firewall Rate Limiting:** Limit SYN packets per source IP
- **TCP Intercept:** Router intercepts and validates connections
- **Increased Backlog Queue:** More space for half-open connections

### Against UDP Flood:

- **Rate Limiting:** Limit UDP packets per second
- **Firewall Rules:** Drop UDP to unnecessary ports
- **Traffic Anomaly Detection:** Identify and block unusual patterns
- **CDN/DDoS Protection:** Absorb traffic before it reaches your server

---

## 📚 Want to Learn More?

If this lab sparked your interest, continue your journey:

- **Metasploitable Documentation** — [rapid7.com](https://docs.rapid7.com/metasploit/metasploitable-2/) — Learn about all the vulnerabilities
- **Wireshark User Guide** — [wireshark.org](https://www.wireshark.org/docs/wsug_html_chunked/) — Master packet analysis
- **Scapy Official Docs** — [scapy.readthedocs.io](https://scapy.readthedocs.io/) — Build any packet you can imagine
- **TryHackMe** — [tryhackme.com](https://tryhackme.com) — Free cybersecurity labs
- **Hack The Box** — [hackthebox.com](https://www.hackthebox.com) — Practice offensive security
- **TCP/IP Guide** — [tcpipguide.com](http://www.tcpipguide.com/) — Deep dive into networking protocols

---

## 🎯 Summary — The 5 Simple Steps

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   1. SETUP NETWORK     →  Create Host-Only network in VBox  │
│                                                             │
│   2. FIND IP           →  Login to VM, run `ip addr show`   │
│                                                             │
│   3. START WIRESHARK   →  Capture on vboxnet0 interface     │
│                                                             │
│   4. RUN ATTACK        →  Execute SYN/UDP flood scripts     │
│                                                             │
│   5. ANALYZE           →  Apply Wireshark filters & study   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

*Simple DDoS Lab Guide — A Hands-On Introduction to DDoS Attack Analysis*  
*Built for cybersecurity learners and network security students* 🔐
