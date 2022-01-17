from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
from lxml import html
import requests
import re
import pprint
import json


def crea_associazione_Sector_Industry():    # NON PIU' UTILE
    # xpath "esatto": /html/body/div[1]/div[5]/div[5]/table/tbody/tr/td[1]/a

    # root = 'https://www.macrotrends.net'
    # stringa_xpath = '//div[5]/table/tbody/tr/td[1]/a'
    # pag = requests.get('https://www.macrotrends.net/stocks/research').text
    # contenuto = html.fromstring(pag)
    # lista = contenuto.xpath(stringa_xpath)
    # sectors = list(map(lambda x: (x.text, root + x.attrib['href']), lista))

    # '/html/body/div[1]/div[5]/div/div/div/div[4]/div[2]/div/div[1]/div[1]/div/a'
    # '/html/body/div[1]/div[5]/div/div/div/div[4]/div[2]/div/div[2]/div[1]/div/a'
    root = 'https://www.macrotrends.net'
    stringa_xpath = "//div[id='row1jqxgrid_sector_10']"
    pag = requests.get('https://www.macrotrends.net/stocks/sector/10/computer-and-technology').text
    contenuto = html.fromstring(pag)
    lista = contenuto.xpath(stringa_xpath)
    industries = list(map(lambda x: x.text, lista))
    print(lista, industries)
    with open("verifica.html", 'w') as f:
        f.write(pag)
    f.close()


def estrae_elenco_azioni():
    with open('../Elenco_azioni/The Web', 'rt') as f:
        pagina = f.read()
    f.close()
    sigle_azioni = re.findall(r'ticker\":\"(.+?)\"', pagina)
    nomi_azioni = re.findall(r'comp_name_2\":\"(.+?)\"', pagina)
    industrie = re.findall(r'zacks_x_ind_desc\":\"(.+?)\"', pagina)
    settori = re.findall(r'zacks_x_sector_desc\":\"(.+?)\"', pagina)
    industrie = list(map(lambda x: x.replace('\\/', '/'), industrie))
    settori = list(map(lambda x: x.replace('\\/', '/'), settori))
    records = [(azione, nomi_azioni[n], industrie[n], settori[n]) for n, azione in enumerate(sigle_azioni)]
    records.sort(key=lambda record: record[0])
    with open('../Elenco_azioni/Elenco_azioni.json', 'wt') as output_file:
        json.dump(records, output_file)


def scarica_serie_storiche():   # da aggiungere una gestione degli errori

    directory_di_lavoro = './Elenco_azioni'

    file_di_log = directory_di_lavoro + '/azioni_scaricate.log'
    f_log = open(file_di_log, 'rt')
    ultima_azione_scaricata = str(f_log.readline()).strip('\n')
    f_log.close()
    f_log = open(file_di_log, 'at')

    while True:
        input_tastiera = input("Numero di azioni da scaricare? ")
        try:
            numero_azioni_da_scaricare = int(input_tastiera)
            break
        except:
            print("input non corretto")
    prima_azione = int(ultima_azione_scaricata) + 1
    with open(directory_di_lavoro + '/Elenco_azioni.json') as f0:
        elenco_azioni = json.load(f0)
    f0.close()
    ultima_azione = min(len(elenco_azioni), prima_azione + int(numero_azioni_da_scaricare))

    opts = Options()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', 'C:/')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    browser = Firefox(options=opts, firefox_profile=profile)

    for n, azione in enumerate(elenco_azioni[prima_azione:ultima_azione]):
        sigla_azione = azione[0]
        pagina = 'https://www.macrotrends.net/assets/php/stock_price_history.php?t=' + sigla_azione
        messaggio_log = ''
        try:
            browser.get(pagina)
            download_elements = browser.find_element_by_xpath("/html/body/div/div[1]/div[4]/div/button")
            download_elements.click()
            messaggio_log = ' '.join([str(prima_azione + n), azione[0], azione[1], '... scaricata'])
        except:
            messaggio_log = ' '.join(['ERRORE:', str(prima_azione + n), azione[0], azione[1], '... NON scaricata'])
        print(messaggio_log)
        f_log.writelines(messaggio_log+'\n')

    f_log.close()
    f_log = open(file_di_log, "r+")
    f_log.seek(0)
    f_log.write(str(prima_azione + n))
    f_log.close()

    browser.close()


scarica_serie_storiche()
print("OPERAZIONE COMPLETATA")
exit(0)
