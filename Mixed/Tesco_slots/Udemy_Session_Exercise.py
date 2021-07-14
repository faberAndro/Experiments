'''
1. Faccio una prima richiesta inviando le cookies che prendo da una richiesta fatta col browser, e nello specifico le prendo da un file su cui le ho salvate.
2. La richiesta che faccio deve avvenire tramite "Session" e "get". A questo punto posso salvare in una cache le cookies della Session
3. Più tardi faccio una nuova request all'interno della stessa Session

4. Ogni volta che faccio una richiesta stamo a schermo con xpath un parametro che posso avere solo sulla mia pagina personalizzata

5. Quando finisco salvo le ultime cookies nel file "f", e le caricherò alla riapertura successiva
6. Rifaccio lo stesso ciclo senza cookies (uso una variabile di controllo all'inizio del codice) e controllo che la richiesta di xpath stavolta mi dia una lista vuota.

'''
import requests
from http import cookiejar as cj

webpage = "https://www.udemy.com/"
s1 = requests.get(webpage)
jar1 = s1.cookies
print(jar1)

s2 = requests.get(webpage, cookies=jar1)
jar2 = s2.cookies
print(jar2)



