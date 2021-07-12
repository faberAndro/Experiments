import subprocess
import os
import time

def check_connessione():
    result = subprocess.run('ipconfig /all', stdout=subprocess.PIPE)
    esito = str(result.stdout)
    esito_ = esito.replace('\\r\\n', '\n').replace('\\x8d', 'ì')
    # usare regex su esito e salvare nella variabile "controllo"
    if controllo == ... # qualcosa:
        return True
    else:
        return False

os.chdir(r'C:\Program Files (x86)\NordVPN')
subprocess.run('nordvpn -c')

conneesso = False
while connesso:
    time.sleep(60)
    check_connessione()