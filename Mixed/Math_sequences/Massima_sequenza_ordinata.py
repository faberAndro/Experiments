# troviamo la lunghezza della massima sotto-sequenza di "sequence" ordinata in senso crescente stretto


def funzione(sequence):
    from itertools import combinations
    lista = ''
    lunghezza = len(sequence)
    for n0 in range(lunghezza):
        n = lunghezza-n0
        subsequences = list(combinations(sequence,n))
        for tupla in subsequences:
            candidato = True
            for x in range(1,len(tupla)):
                if tupla[x] <= tupla[x-1]: 
                    candidato = False
                    break
            if candidato == True:
                print(tupla)
                return n
    return 1

lista = [1000000000,22,9,33,21,50,41,60,80,90,90,100,103,108,105]
r = funzione(lista)
print(r)
