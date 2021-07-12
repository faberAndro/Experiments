#!/usr/bin/python3.7

import socket
import optparse


# LA FUNZIONE socket.socket.recv() SCARICA I DATI DALLA PORTA A CUI CI SI E' CONNESSI
def retBanner(ip, port):
    try:
        # s2 = socket(AF_INET, SOCK_STREAM)
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        # s.connect_ex()
        # socket.gethostbyaddr('8.8.8.8')
        # socket.gethostbyname('www.fabriziobernini.webnode.it')
        banner = s.recv(1024)
        # s.close()
        return banner
    except:
        return


def main():
    # ACQUISIZIONE DEI PARAMETRI AGGIUNTIVI DA TERMINALE
    parser = optparse.OptionParser("Opzioni =   -I: Ip address, -P: Port")
    parser.add_option('-I', dest='ip', type='string', help='immettere l\'indirizzo IP')
    parser.add_option('-P', dest='porta', type='int', help='immettere la porta di inizio')
    (opzioni, args) = parser.parse_args()
    ip, porta = opzioni.ip, opzioni.porta

    ip = "172.67.1.1"
    print(ip)
    #ip = "192.168.1.7"
    for port in [25, 80, 113, 143, 443, 587]:
        banner = retBanner(ip, port)
        if banner:  # controlla se la porta ha risposto o no (ossia se il pacchetto di risposta è vuoto o no)
            print("porta", port, ":", banner)
        else:
            print(port)
        

main()
