import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.setdefaulttimeout(2)
lista_porte = (list(range(20, 100))+list(range(180, 500)))

lista_porte = [25, 80, 113, 143, 443, 587]
# ip0 = "77.78.119.20"
ip = "172.67.1.1"
for port in lista_porte:
    try:
        conn = s.connect((ip, port))
        print('Port', port, 'is open')
        dati = s.recv(1024)
        print(dati)
    except :
        print('Port', port, 'is closed - ')


# s.connect_ex( (host,port) ) ....