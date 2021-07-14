import math
import time

def ricorri(n,x,lista_divisori):

    if (n==x):
        f = float(x)
        f2 = math.sqrt(f)
        f3 = math.floor(f2)
    else:
        f=f3=int(x)
        
    for i in range(2,f3+1):
        #print("divisore: ",i,"\t",f%i)
        if ((f%i)==0):
            n2 = f/i
            lista_divisori.append(int(i))
            
            p = 1
            for j in lista_divisori:
                p *= j
            #print(p)
            if (p==n):                
                return lista_divisori
                break
            else:
                p2 = ricorri(n,n2,lista_divisori)
                p = 1
                for j in p2:
                    p *= j
                    #print(p)
                    if (p==n):   
                        return lista_divisori
                        break
                    
    return lista_divisori       

def main():
    
    primo = 100000121335352
    isSemiprime = None
    lista1 = []
    lista = ricorri(primo,primo,lista1)
    print(lista)
    if len(lista)==2:
        isSemiprime = True
    else:
        isSemiprime = False
    print(isSemiprime)
    
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))