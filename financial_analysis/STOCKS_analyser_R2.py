# coding=utf-8
import pandas as pd

file_name = r'C:\04. IT Projects\PROJECTS\0. AI Projects/NEWS_ANALYTICS/SA_machine/Stocks_list_MTD/MacroTrends_Data_Download_A.csv'

# CARICA I DATI STORICI DI UN AZIONE
time_series = pd.read_csv(file_name, header=9)
data_frame = time_series[['date', 'open']]  # in questo caso il valore è il prezzo di apertura, ma si può scegliere anche come media dei 4 prezzi
ts = time_series[time_series.columns.to_list()[1:-1]]
# INDICATORI:
# kurtosis:

krt = data_frame.kurtosis()
# implementing a CCI (vettorizzare. Ogni funzione va sostituita da una nuova serie di pandas/numpy):
P = 20
start = 2*P


def tp(ts, time):
    return sum((ts.high + ts.low + ts.close)[time-P: time])/3/P


def MA(ts, time):
    MA = 0
    for t in range(P):
        MA += tp(ts, time - t)
    return MA/P


def MD(ts, time):
    MD = 0
    for t in range(P):
        MD += abs(tp(ts, time - t) - MA(ts, time - t))
    return MD/P


def CCI(ts, time):
    return (tp(ts, time) - MA(ts, time)) / (0.015 * MD(ts, time))


# RIORGANIZZA I DATI USANDO UNA FINESTRA MOBILE
W = 45  # considera i dati 'x' dall'ultimo mese e mezzo
# scegliamo 'y' come il massimo delle due settimane futura
# in questo caso conta l'ordine delle features, quindi bisognerebbe usare una RNN. Sono come parole di un libro.
# una serie storica è come un brano di un libro, e la settimana successiva è la predizione
# possiamo considerare una serie di parametri invece che i singoli punti della serie:
"""
1. numero e lunghezza di pendenze negative abbastanza lunghe
2. numero e lunghezza di pendenze positive abbastanza lunghe
3. percentuale di variazione sul periodo
4. andare nel passato con un algoritmo logaritmico. Più si va indietro, 
più si applica un peso minore alle statistiche.
5. Numero ed estensione dei flessi
praticamente estraiamo i parametri principali della funzione.
L'ordine di questi parametri conta.
IN POCHE PAROLE ANALIZZIAMO LA FUNZIONE MATEMATICAMENTE E NE ESTRAIAMO LE SEQUENZE DI VALORI PRINCIPALI
PRIMA COSA DA FARE: approssimare l'andamento con una serie di spezzate lineari. Così diminuiamo il numero di dati, 
preservando però l'informazione.
"""

