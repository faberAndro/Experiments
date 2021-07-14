import matplotlib.pyplot as plt
import numpy as np
from numpy import math as m 
from scipy.stats import binom

v = True
X0 = 100 # SOMMA INIZIALE
N_giocatori = 10000
    
n  = 100
n1 = 1
n2 = 100
p = 0.5

k = np.arange(0,n+1)
prob = np.arange(binom.pmf(0, n, p), binom.pmf(n, n, p))
plt.plot(k,prob)
plt.show()

input()
valore = (0.9**k) * (1.11**(n-k)) * X0
distribuzione = prob * valore
    
plt.plot(k,prob)
plt.plot(k,valore/X0)
#plt.plot(x,elemento)
soglia = N*np.log(1.11) / (np.log(1.11)-np.log(0.9))
#print(soglia)
#plt.plot(valore, prob*N_giocatori)  # QUESTO E' IL GRAFICO PIU' SIGNIFICATIVO, MA NEL CICLO FOR BISOGNA METTERE SOLO UN VALORE, ALTRIMENTI DISEGNA TROPPI GRAFICI
plt.show()

if v:
    print(N,'\t','giocatori che guadaganano:','\t',N_giocatori*sum(prob[:int(np.floor(soglia))]))
#print(N,'\t',sum(elemento)*X0)


