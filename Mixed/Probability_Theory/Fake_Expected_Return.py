import matplotlib.pyplot as plt
import numpy as np
from numpy import math as m 

def f(i):
    a = np.arange(1,i+1)
    b = a.prod()
    return b

def Bnk(n):
    r = []
    for k in range(n):
        fact = 1
        for kappa in range(1,k+1):
            fact *= (n-kappa+1)/(kappa)
        r.append(fact)
    r.append(1)
    nr = np.array(r)
    return nr

v = True
X0 = 100
N_giocatori = 10000

for N in range(22,23):
    k0 = np.arange(1,2).reshape((1,1))
    k1 = np.arange(1,N+1).reshape((1,N))
    k = np.append(k0,k1)
    k2 = np.arange(0,N+1)

#    if v:
#        print(k)
#    k_fact = k.cumprod()
#    n_su_k = f(N) / (k_fact * np.flip(k_fact))
#    if v:
#        print(n_su_k)
    
    prob = Bnk(N) * (0.5**N)
    valore = (0.9**k2) * (1.11**(N-k2)) * X0
    x = range(0,N+1)
    elemento = prob * valore
    
    
    plt.plot(x,prob)
    plt.plot(x,valore/X0)
    #plt.plot(x,elemento)
    soglia = N*np.log(1.11) / (np.log(1.11)-np.log(0.9))
    #print(soglia)
    #plt.plot(valore, prob*N_giocatori)  # QUESTO E' IL GRAFICO PIU' SIGNIFICATIVO, MA NEL CICLO FOR BISOGNA METTERE SOLO UN VALORE, ALTRIMENTI DISEGNA TROPPI GRAFICI
    plt.show()
    
    if v:
        print(N,'\t','giocatori che guadaganano:','\t',N_giocatori*sum(prob[:int(np.floor(soglia))]))
    #print(N,'\t',sum(elemento)*X0)
'''
si può migliorare riducendo a metà computo il calcolo di n_k, data la simmetria
i numeri diventano troppo grandi a cumprod non ce la fa.
'''


