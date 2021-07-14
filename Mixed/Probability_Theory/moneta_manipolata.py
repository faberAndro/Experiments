# testa: 0
# croce: 1
import time
import random

n_teste_Sofia = 0 
n_croci_Sofia = 0
n_lanci_Sofia = 0
sofia_mostra = True
teste_mostrate = 0
croci_mostrate = 0
lanci_mostrati = 1
v = 0

while True:

    lancio_Sofia = round(random.random()) 
    lancio_Tom = round(random.random())

    if (lancio_Sofia == 0):
        n_teste_Sofia += 1
    else:
        n_croci_Sofia += 1
    n_lanci_Sofia += 1
    
    r = teste_mostrate/lanci_mostrati
    if r > 0.37:
        if lancio_Sofia == 0:
            sofia_mostra = False     
        else:
            sofia_mostra = True
    else:
        if lancio_Sofia == 0:
            sofia_mostra = True     
        else:
            sofia_mostra = False
    
    if sofia_mostra:
        lanci_mostrati += 1
        if (lancio_Sofia == 0):
            teste_mostrate +=1
        else:
            croci_mostrate +=1
    
        if (lancio_Sofia != lancio_Tom):
            v -= 2
        elif lancio_Sofia == 0:
            v += 3
        else:
            v += 1
    
    if lanci_mostrati != 0:
        rm = teste_mostrate / lanci_mostrati
    else:
        rm = 0
    rs = '%.2f' % rm
    output = str(lancio_Sofia) +'\tT:' + str(n_teste_Sofia) +'\tC:' + str(n_croci_Sofia) + '\tTM:' + str(teste_mostrate)+ '\tCM:' + str(croci_mostrate) + '\tr:' + rs + '\tTomVince:' + str(v)
    print(output)
    #time.sleep(0.1)
