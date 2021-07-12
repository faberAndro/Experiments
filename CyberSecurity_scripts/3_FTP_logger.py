#!/usr/bin/python

import ftplib

anonymous = True

def ftp_Login(hostname, username, password):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login(username, password)
        print(hostname + ' FTP Logon succeeded')
        print('user: ',username,'pwd: ',password)
        ftp.quit()
        return True
    except Exception, e:
        print(hostname + ' FTP Logon failed')
        
host = input('Enter target IP address: ")
if not anonymous:
    username = input("Enter USER: ")
    password = input("Enter PWD: ")
else:
    username = 'anonymous'
    username = 'anonymous'

ftp_Login(host)