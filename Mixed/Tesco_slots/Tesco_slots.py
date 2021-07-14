from lxml import html
import requests
import json
import datetime
import time

def analizzaCategoria(categoria, link):  
    
    tab = '\t\t'
    testi = tree.xpath(categoria)
    links = tree.xpath(link)
    if test:        
        print(testi,'\n',len(testi),'\n')
        print(links,'\n',len(links),'\n')
    numero = 1
    n = str(numero)
    testi_depurati = []
    
    for x1 in testi:
        x2 = x1.strip()        
        x3 = x2.replace('\n','')
        if bool(x3):
            pagina_L = links[numero-1]
            if pagina_L[0] == '/':
                pagina_L = root + pagina_L
            stringa = tab+n+': '+x3+'\t\t\t'+pagina_L+'\n'
            testi_depurati.append(stringa)
            numero += 1 
        n = str(numero)

    numeroNotizie = len(testi_depurati)

    for x in testi_depurati:
        notizia = testi_depurati.index(x)
        try:
            f2.write(x)
        except:
            f2.write(tab+str(notizia+1)+': caratteri illeggibili'+'\n')            

        if not test:
            print("Pagina Web: ",nP+1,"/",numeroPagineWeb, " --- chiave: ",nCR+1,"/",numeroChiaviRicerca," --- notizia: ",notizia+1,"/",numeroNotizie, end='    \r')
        # time.sleep(0.03)
                
#######################################

def main():
    
    global test
    test = True
    
    global root, webpage, numeroPagineWeb, f2, tree, numeroChiaviRicerca, nP, nCR

    if test:
        nome_sito = "https://www.tesco.com/groceries/en-GB/slots/delivery"
        input_file = r'.\Downloaded_Pages\CNN\https _edition.cnn.com_.html'
        root = 'https://www.ansa.it'
        nome = "news-title area-primopiano"
#        descrizione = "//html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[1]/section//article/header/h3/a/text()"
#        collegamento = "//html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[1]/section//article/header/h3/a/@href"
        descrizione = "//article/header/h3[@class='news-title area-primopiano']/a/text()"
        collegamento = "//article/header/h3[@class='news-title area-primopiano']/a/@href"
        f1 = open(input_file, 'rt', encoding='UTF-8')
        p = f1.read()
        tree = html.fromstring(p)
        # LEGGE E SCRIVE I DATI
        output_file = r'.\News_Analysis\TEST_Analysis_' + nome_sito + "_" + str(datetime.date.today()) +'.txt'
        try:
            f2 = open(output_file, 'w')
        except:
            print("file: ",output_file,"già esistente o errore in apertura")   
        f2.write('Classe di test: '+nome+'\n')
        analizzaCategoria(descrizione, collegamento)        
        f2.close()
    
    
    if not test:
        # CARICA LA LISTA DEI SITI DA ANALIZZARE
        file_di_elenco = ".\\News_Source_Index.json"
        f1 = open(file_di_elenco)
        elenco_fonti = f1.read()
        webpages = json.loads(elenco_fonti)
        pagine = webpages["webpages"]
        numeroPagineWeb = len(pagine)

        # LEGGE I DATI
        output_file = 'News_Analysis_'+str(datetime.date.today())+'.txt'
        try:
            f2 = open(output_file, 'w')
        except:
            print("file: ",output_file,"già esistente o errore in apertura") 

        for pagina in pagine:
            #print(pagina)
            #input()
            root = pagina["root"]
            webpage = pagina["webpage"]
            w = requests.get(webpage)
            p = w.text            
            tree = html.fromstring(p)
            # meglio sarebbe fare questo utilizzando gli axes di XPath
            f2.writelines(['\n',webpage])
            f2.writelines(['\t',pagina["categoria"]])
            chiavi = pagina["chiavi_di_ricerca"]
            numeroChiaviRicerca = len(chiavi)
            for ricerca in chiavi:
                f2.writelines(['\n\tCategoria ',ricerca["nome"],'\n'])
                nP  = pagine.index(pagina)
                nCR = chiavi.index(ricerca)
                analizzaCategoria(ricerca["descrizione"], ricerca["collegamento"])        

        # SHOWING ANALYSIS PROGRESS
        print('\n')
        f2.close()

if __name__ == '__main__':
    main()