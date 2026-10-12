---
name: scapy
description: Inspect selected TCP packet payloads in an acquired capture with Scapy's offline Python API. Use when endpoint/direction boundaries and packet concatenation must be distinguished from stream reassembly.
---

# Preserve packet boundaries during offline inspection

Read this entire SKILL.md before acting. Require a trusted Python environment with Scapy already installed, the saved capture and selected endpoint/port. No conditional resources are required. Finish with packet records, status and capture/reassembly limits; no match is not proof of no traffic.

Define `python_bin`, `pcap`, numeric `peer` and positive TCP `port`; define `records` as a fresh private output. This reads offline and emits matching IPv4/IPv6 packet payloads without sending packets:

~~~bash
umask 077
"$python_bin" -I - "$pcap" "$peer" "$port" >"$records" <<'PY'
import json
import sys
from scapy.all import IP, IPv6, TCP, sniff
capture, peer, port_text = sys.argv[1:]
port = int(port_text)
if not 1 <= port <= 65535:
    raise ValueError("invalid TCP port")
number = 0
def inspect(packet):
    global number
    number += 1
    net = packet.getlayer(IP) or packet.getlayer(IPv6)
    if net is None or TCP not in packet:
        return
    tcp = packet[TCP]
    if peer not in (net.src, net.dst) or port not in (tcp.sport, tcp.dport):
        return
    payload = bytes(tcp.payload)
    print(json.dumps({"packet": number, "time": str(packet.time),
        "src": net.src, "sport": tcp.sport, "dst": net.dst,
        "dport": tcp.dport, "seq": tcp.seq, "ack": tcp.ack,
        "flags": str(tcp.flags), "payload_bytes": len(payload),
        "payload_hex": payload.hex()}))
sniff(offline=capture, prn=inspect, store=False)
PY
~~~

Keep status/stderr and the original capture. `store=False` avoids accumulating a packet list; output can still be large. A failure leaves partial records. Normalize the peer to the capture's address representation if matching fails.

Port equality alone can merge unrelated flows. Separate endpoints, direction and connection lifetime; retransmissions, reordered/missing segments, fragmentation and truncated frames prevent simple payload concatenation from establishing an exact TCP stream. This procedure retains packet bytes, not reassembly. For a required application stream, use a compatible protocol-aware reassembler and check gaps. Scapy's TCPSession supports selected protocols and requires an appropriate `tcp_reassemble` implementation; enabling it is not generic arbitrary-protocol recovery.

Sources: [offline sniff API](https://scapy.readthedocs.io/en/latest/api/scapy.sendrecv.html#scapy.sendrecv.sniff), [sessions and reassembly](https://scapy.readthedocs.io/en/latest/usage.html#advanced-sniffing-sniffing-sessions).
