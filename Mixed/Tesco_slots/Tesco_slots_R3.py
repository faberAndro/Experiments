'''
# method to test (alternative to Sessions):

jar = requests.cookies.RequestsCookieJar()
tesco1 = requests.get(some_url, cookies=jar) # or post ...
jar.update(tesco1.cookies)
tesco2 = requests.get(some_other_url, cookies=jar) # or post ...
'''

import random
import datetime as dt
import time
import requests
from lxml import html
from http.cookies import SimpleCookie as ck
# import cookielib
# import pprint
# from multiprocessing import Process

t_ciclo = 10 # in secondi
t_random = 2 # in secondi

def trova_riga_orari(tree):
    slot_1 = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/ul/li[1]/a/text()'
    slot_2 = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/ul/li[2]/a/text()'
    slot_3 = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/ul/li[3]/a/text()'
    w1 = tree.xpath(slot_1)
    w2 = tree.xpath(slot_2)
    w3 = tree.xpath(slot_3)
    ora = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    slots = str(w1) + '   ' + str(w2) + '   ' + str(w3)
    risultato = ora + '->' + '\t' + slots 
    return slots, risultato
    
output_file = 'TESCO_orari_aggiornamento_Slot' + str(dt.date.today()) + '.txt'
cookies_T     = "trkid=3f99fda4-2f71-4c23-95b5-2550fbf2d972; atrc=c54d4605-3201-41d5-8678-807f5e5658b7; h-e=0ab87a633b04141c9dd61b9546c44349a198a9d0914b17963565a369dce95929; cookiesAccepted=1584296666851; consumer=default; DCO=wdc; HYF=0; ighs-sess=eyJwYXNzcG9ydCI6eyJ1c2VyIjp7ImlkIjoiZTU5OTcxOWMtN2RkMy00ZDNlLWExZmQtZThjMDhjOTMxYTIxIn19LCJzdG9yZUlkIjoiMzMyNCIsImFuYWx5dGljc1Nlc3Npb25JZCI6IjhlOGRjNmY0YzA5NGQ2ZDIwMWIzMjRjZGFjNjdkZWRhIn0=; ighs-sess.sig=OP28Ks8NQjVxfRCf82AlAttSwbo; itemsPerPage=48; waitingRoom=%7B%22key%22%3A%2220170825001%22%2C%22access%22%3A%22GRANTED%22%2C%22granted%22%3A1585932773%2C%22ttl%22%3A1585932832547%2C%22uuid%22%3A%221585932772522-5844776%22%2C%22hash%22%3A%225c6cba0f%22%2C%22queueingSince%22%3A1585932772547%7D; atrc=c54d4605-3201-41d5-8678-807f5e5658b7; _abck=205D43C83190CA72CF3B5D5CF1DF371E~-1~YAAQRTMHYGk1jTpxAQAAE6r1QAMDyxS6nm2MjVhgOdJCzeRmDoWsNoeiAQ27DeqxDPOVtGVFkVN1ynowDcJpnBZRicS2MZLDdyiY/aGN5bFpRYCGuSRpM1v7mpxN743JS0lo+O17dSBG3LRNYIf7wRxaiLC/Idn6s7/LJy/ilzWUiqLCxQ9wgMzEAHmLQAUsKhqN3lNTjRLExtSfbIvvFiTKjYEA6DVPq5wAZoxm30AIlIsmj3VCL0o1e04AGRnHYibnBo+oRtRjYLMhGgqw/5Qh0e6mO7w5URgqsR1+kIxH3q5LPIxRHx8l7mvTVJJ5huzF9EEy~0~-1~-1; AMCV_E4860C0F53CE56C40A490D45%40AdobeOrg=-1712354808%7CMCIDTS%7C18356%7CMCMID%7C34022507114548101124614441961596193192%7CMCAID%7C2F3738FF0515D2C6-60000A84059909A7%7CMCOPTOUT-1585940058s%7CNONE%7CMCAAMLH-1586537658%7C6%7CMCAAMB-1586537658%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C4.3.0%7CMCSYNCSOP%7C411-18359; s_vi=[CS]v1|2F3738FF0515D2C6-60000A84059909A7[CE]; s_ecid=MCMID%7C34022507114548101124614441961596193192; s_nr=1585932858660-Repeat; _ga=GA1.2.1721522818.1584296627; __gads=ID=6a49320174b03992:T=1584296555:S=ALNI_MZNm8ENgymucZ8-3eOcU_CpkrD4zQ; __sonar=17185570176616520030; _gcl_au=1.1.1505187641.1584296669; _fbp=fb.1.1584296669374.911138877; _4c_=jVPbTttAEP0VtA88YXvvl0hRlQBBrQSIXtTHyPYuZBUTW14nJkX5d2YTJ0WlquoXe2bPHM%2BcOfuK%2BoVboRERWhhGtVIKswu0dNuARq%2Bo9Ta%2BNmiE8kIrI9RjYkpnE14wmWhtZIK5zZnRRa6YQBfoJXIZihWV0hAsdxeobAaOV7RuK6BadF0TRlnW933auVDWaVk%2FZ09tXbrWu5C5VXIzzUJVdyGzrvIb126Buqytg2piUpMyiLtfEEkMX01b23XZzbttExG9K86CXcKBdRtfunnvbbeIpYLJ39mF80%2BLDtJa8pht2ghJaRyj9ytb938WDtlTIdsXNlW%2B7V0VJ7uDsGjrPrjINfOte6xfzlRE1SAo%2BrknCBDCiWvbPQyi4LvY%2BEmMIQVrOGYtcJVdsl4m9appXUTc337%2FOp9eTy7v796JGp5d1%2FoyvFO2yELI9uF6eVI5apaR7Mu3hKZEpTi5Ug93WSBGgREI01IRJT5NHqZjcv7s7ZhxTKnAihAuuCaYEMol4ZwTI2HjkkCVoec5QOmMKaZnMyyIuKKXMpEYnonmWBiDzUSdTx6uxyRKF51lFHxVdZlXUQNwIwwPs%2FoafIkO%2Fcb130zmPz5fxWUoSgSlmugUbMupkZKqox63l3vM%2F3WLdoNhtcQQSgkdgq86WCV4IjaNd4cm9%2F416gOcfYQf9j%2F0%2Fa%2Fav%2F2qGuDkiIZlCI45o2ZAwxBH9MYfLyfcWkqwdonFJVxOLVliCpMn1DgOJIYxx9A7Si6lZOpEqQ%2BMu90b; cookiesAccepted=1585932776716; updatedCookiesAccepted=1; _csrf=Jt1RbNqpkbo8g67s1Tk4Cs92; AMCVS_E4860C0F53CE56C40A490D45%40AdobeOrg=1; _gid=GA1.2.1773623775.1585778907; s_cc=true; s_sq=%5B%5BB%5D%5D; ADRUM=s=1585932877701&r=https%3A%2F%2Fwww.tesco.com%2Fgroceries%2Fen-GB%2Fslots%2Fdelivery%3F0; mytesco_from=https%3A%2F%2Fwww.tesco.com%2Fgroceries%2Fen-GB%2Fslots%2Fdelivery; akavpau_tesco_groceries=1585933077~id=13b5685fd48143088c2a76d44e34afe1; s_fid=4898B91341D310CF-361FF9B31D12325F; UUID=9464c104-de6a-4dbc-8b55-1dbb560dfd6e; CID=117449061; trm=%2BDzOp5jGHyOvsFbgTIXrhulPFA3ZWdXDPgFlzjtY4oniQHW5ZjRWKUVeYtSvdliyRpX9qbDDy0JmaVn2Aurx0IFSancBrO3blZWiuwLrWivnTn9lxi8VFo7R%2B0NUg9ewmFp1XLiObF%2F2BOkpADsP2xdG6WwCRNceSuElMR3VZqUggUWRiK1xFLK5VuhJKSD%2BDF7yqVUz; bm_sz=142283C8169826A9D6AEAE34E5B494AC~YAAQdo57XLjawy9xAQAAQH9AQAeivVLvMedZASmMSKXyBo/27Texsewbj/N1qXsB9LffGSp/VU/VMtn+w4CZywsaYrD8zdx5BKbKzXXYEIlccI2O54Rk2HFFMo2zjZf3Fo1S0cNZeqw/tmhvmi1ycncH2n6dz0HYs7FguzEXU7MwXqrPH/f5r/KUf9qX9wI=; DCACC=AWS1; s_gpv_pn=login; OAuth.AccessToken=e599719c-7dd3-4d3e-a1fd-e8c08c931a21; OAuth.TokensExpiryTime=%7B%22AccessToken%22%3A1585936372129%2C%22RefreshToken%22%3A1585939972129%7D; s_prevpage=slots%3Adelivery; _gat_ukLego=1"
cache_slots = ''
prima_richiesta = True

while True:
    # IMPOSTA LE COOKIES DA MANDARE A TESCO
    cook_S = ck(cookies_T)
    cook_D = {}
    for key, morsel in cook_S.items():
        cook_D[key] = morsel.value
    # pprint.pprint(cook_D)
    
    # SI CONNETTE INVIANDO LE COOKIES
    page = "https://www.tesco.com/groceries/en-GB/slots/delivery"    
    # tescoSession = requests.Session()
    if (prima_richiesta):
        jar = requests.cookies.RequestsCookieJar()
        tesco = requests.get(page, cookies = cook_D)
    else:
        if (tesco.history): # we have to add to the cookie jar, the cookies sent by the server in intermediate responses
            for historictesco in tesco.history:
                jar.update(historictesco.cookies)      
        tesco = requests.get(page)
        
    # ANALIZZA LA PAGINA ED ESTRAE I 3 SLOTS
    pagina = tesco.text
    tree = html.fromstring(pagina)    
    slots, testoTrovato = trova_riga_orari(tree)
    print(testoTrovato)

    try:
        f = open(output_file, 'at')
        f.writelines(testoTrovato+'\n')
        f.close()
    except:
        print("file: ",output_file,"errore in apertura del file") 

    if (not prima_richiesta) and (slots != cache_slots):
        break    
    prima_richiesta = False
    
    # MEMORIZZA slots precedenti e cookies ricevuti nella cache
    cache_slots = slots;
    # cookies_T = dict(tesco.cookies)
    
    # ASPETTA IL TEMPO PREVISTO PRIMA DELLA PROSSIMA RICHIESTA
    deltaT = t_random/2 * (0.5 - random.random())
    time.sleep(t_ciclo + round(deltaT))     


print("programma terminato / premi un tasto per uscire. Orari salvati su file")
x = input()
