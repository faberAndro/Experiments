"""
This module downloads equity timeseries from www.macrotrends.net,
making Selenium to work on top of Firefox browser.
Equity timeseries are saved to C:/ (they have to be moved manually due to a Selenium bug)
"""

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from lxml import html
import requests
import re
import json
from settings import MTD_STOCKS_METAINFO, MTD_EQUITY_LIST_FILE, MTD_LOG_FILE


def parse_stock_list() -> []:
    with open(MTD_STOCKS_METAINFO + 'The Web\'s Best Free Stock Screener MacroTrends.html', 'rt') as f:
        pagina = f.read()
    f.close()
    individual_equities = re.findall(r'ticker\":\"(.+?)\"', pagina)
    equity_names = re.findall(r'comp_name_2\":\"(.+?)\"', pagina)
    industries = re.findall(r'zacks_x_ind_desc\":\"(.+?)\"', pagina)
    sectors = re.findall(r'zacks_x_sector_desc\":\"(.+?)\"', pagina)
    industries = list(map(lambda x: x.replace('\\/', '/'), industries))
    sectors = list(map(lambda x: x.replace('\\/', '/'), sectors))
    records = [(equity, equity_names[n], industries[n], sectors[n]) for n, equity in enumerate(individual_equities)]
    records.sort(key=lambda record: record[0])
    with open(MTD_EQUITY_LIST_FILE, 'wt') as output_file:
        json.dump(records, output_file)
    return records


def download_equity_timeseries():   # error handling to be added

    # pick up downloading from where left
    f_log = open(MTD_LOG_FILE, 'rt')
    last_equity_downloaded = str(f_log.readline()).strip('\n')
    f_log.close()
    f_log = open(MTD_LOG_FILE, 'at')
    while True:
        keyboard_input = input("Number of equities to download? ")
        try:
            number_of_equities_to_download = int(keyboard_input)
            break
        except:
            print("wrong input")
    first_equity = int(last_equity_downloaded) + 1
    with open(MTD_LOG_FILE) as f0:
        equity_list = json.load(f0)
    f0.close()
    last_equity = min(len(equity_list), first_equity + int(number_of_equities_to_download))

    # setting up parameters for Selenium
    opts = Options()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', 'C:/')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    browser = Firefox(options=opts, firefox_profile=profile)

    # proper downloading process
    n = 0
    for n, equity in enumerate(equity_list[first_equity:last_equity]):
        equity_acronym = equity[0]
        page = 'https://www.macrotrends.net/assets/php/stock_price_history.php?t=' + equity_acronym
        try:
            browser.get(page)
            download_elements = browser.find_element_by_xpath("/html/body/div/div[1]/div[4]/div/button")
            download_elements.click()
            log_message = ' '.join([str(first_equity + n), equity[0], equity[1], '... downloaded'])
        except:
            log_message = ' '.join(['ERRORE:', str(first_equity + n), equity[0], equity[1], '... NOT downloaded'])
        print(log_message)
        f_log.writelines(log_message+'\n')

    # completing operations with log file and Selenium instance
    f_log.close()
    f_log = open(MTD_LOG_FILE, "r+")
    f_log.seek(0)
    f_log.write(str(first_equity + n))
    f_log.close()
    browser.close()


def build_Sector_vs_Industry_association():    # SUPERSEDED
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


if __name__ == '__main__':
    download_equity_timeseries()
    print("DOWNLOADED COMPLETED")
