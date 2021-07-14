# valido ora solo per numeri a 4 cifre massimo. Dobbiamo poi includere anche 10000 e gestire i casi a cifre minori

n0 = input()
n = int(n0)
n1 = str(n)

romani = [['','I','II','III','IV','V','VI','VII','VIII','IX'],
['','X','XX','XXX','XL','L','LX','LXX','LXXX','XC'],
['','C','CC','CCC','CD','D','DC','DCC','DCCC','CM']]

# poi trasformiamo questo in un array
l = len(n1)
cifra = []
numero = []
output = ''

# bastava forse usare split per creare una lista
cifra = [char for char in n1]
numero = [int(char) for char in n1]

m = ''
if l == 4:
    for i in range(0,numero[0]):
        m += 'M'
        output = m
    l2 = 3
else:
    l2 = l

for i in range(l2):
    if l==4:
        cifra_romana = romani[l2-1-i][numero[i+1]]
    else:
        cifra_romana = romani[l2-1-i][numero[i]]        
    output += cifra_romana

if n == 10000:
    output = "MMMMMMMMMM"
    
print(output)