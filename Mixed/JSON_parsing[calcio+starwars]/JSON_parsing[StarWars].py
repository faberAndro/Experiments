import urllib.request
import json

#s = input()
s = 'Luke%20Skywalker'

nome = '%20'.join(s.split())

elenco = r'https://challenges.hackajob.co/swapi/api/people/?search='
elenco += nome
print(elenco)
with urllib.request.urlopen(elenco) as f:
    text = f.read().decode('utf-8')
    print(text)
 #   if type(text)==str:
 #       print('Ha ritornato una stringa!! :)')
    dati = json.loads(text)
    r = dati["results"][0]
    f = r["films"]
    n = len(f)
    
    n = len(dati["results"][0]["films"])
    
    print(n)
    print("EVVIVA!!")
    
    
    