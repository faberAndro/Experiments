# valido ora solo per numeri a 4 cifre massimo. Dobbiamo poi includere anche 10000 e gestire i casi a cifre minori

n0 = input()
n = int(n0)
n1 = str(n)

u_r = ['','I','II','III','IV','V','VI','VII','VIII','IX']
d_r = ['','X','XX','XXX','XL','L','LX','LXX','LXXX','IC']
c_r = ['','C','CC','CCC','CD','D','DC','DCC','DCCC','IM']

# poi trasformiamo questo in un array
l = len(n1)
b = []
    
u0 = n1[l-1]
d0 = n1[l-2]
c0 = n1[l-3]
m0 = n1[l-4]

u1 = int(u0)
d1 = int(d0)
c1 = int(c0)
m1 = int(m0)

m = ''
u = u_r[u1]
d = d_r[d1]
c = c_r[c1]
for i in range(m1):
    m += 'M' 

output = m+c+d+u

print(output)
print(n)