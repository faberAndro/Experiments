import datetime as dt
import time
import requests
from lxml import html
from http.cookies import SimpleCookie as ck
import pprint
# from multiprocessing import Process

unitTest = 2

def trova_riga_orari(tree):
    slot_1 = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/ul/li[1]/a'
    slot_2 = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/ul/li[2]/a'
    slot_3 = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/ul/li[3]/a'
    w1 = tree.xpath(slot_1)
    w2 = tree.xpath(slot_2)
    w3 = tree.xpath(slot_3)
    ora = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    risultato = ora + ':\t' + w1 + '   ' + w2 + '   ' + w3 + '   ' 
    return risultato
    
#def scrive_riga_orari():
    # scrive la riga degli orari con data e ora in cui la prende

if (unitTest == 1):
    file_locale = 'Book a slot - Tesco Groceries.html'
    fl = open(file_locale, 'rt')
    p = fl.read()
    tree = html.fromstring(p)
    slot_1 = '/html/body/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[3]/div[3]/div[1]/ul/li[1]/a/text()'
    testoTrovato = tree.xpath(slot_1)
    print(testoTrovato)
    fl.close()
    
elif (unitTest ==2):
    # IMPOSTA LE COOKIES DA INVIARE CON IL METODO GET
    c = '__cfduid=dadcc23fa15194e095876f619dc235eb51573164670; ud_firstvisit=2019-11-07T22:11:10.475442+00:00:1iSpzi:MCF2nItgxTUIRLP28FtOR8e2UMM; ud_rule_vars=eJx9jkGuwjAMRK9SZQtFtttSN2epFLmpy48-KCJJ2SDuTiUQYsVqFvZ7M3dTJJ206OxuIYcSk0UFD_1xmlGkJfZDM0lHDXeCoLwM1sf4H9TYytxHc5ZcXImr_3MlybIE73Jck1d3kxRkOuu4fY5G5jyaffUGkl5X3XKW8r4T4FAj1tBXRBbRIhw6JgbeAViAL9hv_qyvva6Ey8dAUENbA1bY2aaxRAcaGBm_DUtIm-LF_m5vezzyp_1hHk-7w1hf:1jK3g6:Yi7UXrejCG1jzB_-wAMLfN5eMFg; __udmy_2_v57r=1e0c076bd1aa428c93ba52385a10e8f9; EUCookieMessageShown=false; _ga=GA1.2.186801297.1573164707; _gac_UA-12366301-1=1.1585848686.Cj0KCQjwmpb0BRCBARIsAG7y4zbCbS8fzMsFgEMwpEzNk8WfOGDI0kecg_i8IeAW32BcJh3jqpV9Sp0aAkp6EALw_wcB; _pxvid=80ff45b1-01ab-11ea-9518-8709089f635e; csrftoken=n0k78ltppMO1WBfkF5fROxTJU7F2wPY8bpMFNpzLUeQKjJZiyBjn7ic4xKbmzuwy; _fbp=fb.1.1573164710350.1484453387; stc111655=env:1585848671%7C20200503173111%7C20200402180220%7C2%7C1014616:20210402173220|uid:1573164710484.2118330745.6300414.111655.1595814634:20210402173220|srchist:1014616%3A1584713811%3A20200420141651%7C1014624%3A1584912862%3A20200422213422%7C1069270%3A1584914446%3A20200422220046%7C1014624%3A1585099775%3A20200425012935%7C1069270%3A1585493064%3A20200429144424%7C1014624%3A1585658257%3A20200501123737%7C1069270%3A1585755256%3A20200502153416%7C1014624%3A1585831472%3A20200503124432%7C1014616%3A1585848671%3A20200503173111:20210402173220|nsc:4:20210401154059|tsa:0:20200402180220; ki_t=1573164710510%3B1585831473577%3B1585848740539%3B15%3B93; ki_r=; ken_gclid=Cj0KCQjwmpb0BRCBARIsAG7y4zbCbS8fzMsFgEMwpEzNk8WfOGDI0kecg_i8IeAW32BcJh3jqpV9Sp0aAkp6EALw_wcB; G_ENABLED_IDPS=google; IR_PI=a20170c8-01ab-11ea-abf4-42010a246609%7C1585935140300; ud_last_auth_information="{\"suggested_user_name\": \"Fabrizio\"\054 \"suggested_user_avatar\": \"https://i.udemycdn.com/user/50x50/anonymous_3.png\"\054 \"backend\": \"udemy-auth\"\054 \"suggested_user_email\": \"fabriziobernini@ymail.com\"}:1jFIQz:UFLt2uw6iefPeDQr40nT9vmrEKw"; muxData=mux_viewer_id=469a2e0a-efc5-473c-bab4-69eeb25e0972&msn=0.0003958581692681262&sid=92207c9b-5ea3-4d1b-93b0-2142a5c3ca8e&sst=1585831266734&sex=1585838902258; evi="SlFYNkxYDm4DRRJxTFgObkdREXlCQAMtE0kddlZSCGATQR52VkBPNxMFCXtfTlc6UFERd1tRRTEdURl0XVBXdkpRXWNUU1luRxIJe1hWR3RMXwlzXFNFbgsICTdMWERgEwVKY1RXQHsJDgdjXFdMdBNJUGMYQE99HVFdIExYQ3kHS1Y8QkABK0VRETpMUEN1B1EROkwUV3YAXwk3D0BPegZKGTxCQEd5BEUJexVAA24LQgdjGANXdgdHE3ETH1luVxYJexVAR3oGRQl7FUADbgtCB2MYA1d2B0QfdRMfWW5EF0coGgdXdkpRGXdWUld2SlFdY1RTWW5HEgl7WFVAeEwOB2MeAwxuCwgJc1hVR24LCAk3TFhEYBMFSmNUVEJ/Bw5WbUwKGG4LCAlzWFFNbgsICTdMWERgEwVKY1RUQ3oFDlY8"; dj_session_id=owi3zx37roz7js24mr4sjdbxaifblmo1; __ssid=76fa739d7632e6a1cf9e390dd944997; _ym_uid=1584713812194490656; _ym_d=1584713812; access_token=b96CKNhB9mFdLgzgHkkiU1UcnEHBw9iUtaoAUr3i; ud_user_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NzQ3NzIyOTgsImVtYWlsIjoiZmFicml6aW9iZXJuaW5pQHltYWlsLmNvbSJ9._jdPRpzHtlwMZ-2MvPZmbBvzPi-IuNywkouL59EJhLY; ud_credit_last_seen=None; client_id=bd2565cb7b0c313f5e9bae44961e8db2; intercom-session-sehj53dd=Y2FUU2dUMmwyY1h4dzNETW55R2lQVGlIYVgvMFNCVWo0elB4dml3NWZOMExNSU5GMG1XeVN5bEV2OU5HNWx5MC0tWGVwTTBzSVJ1aC9LWGp3RitYV1RYQT09--7d54e1e3320687876380f6b3486fcc13164e19f9; exaff=%7B%22start_date%22%3A%222020-04-01T15%3A33%3A22.112456Z%22%2C%22code%22%3A%22VkwVKCHWj2A-wytzL2GPGDtiSyjkppLSfw%22%2C%22merchant_id%22%3A39197%2C%22aff_type%22%3A%22LS%22%2C%22aff_id%22%3A38066%7D:1jK3g6:armJ1GslZvwkvmE6JQlzWpzJuC0; rmStore=amid:39197|ald:20200401_1534|atrv:VkwVKCHWj2A-wytzL2GPGDtiSyjkppLSfw; sidebar_content_2310306=default; ud_cache_device=desktop; ud_cache_brand=GBen_US; ud_cache_version=1; ud_cache_price_country=GB; ud_cache_campaign_code=""; ud_cache_modern_browser=1; ud_tgt_ovr="{\"student_provided_deal_visitors\": 21414}:1jK3g6:zzqp9rbpU7xg0AX5zbN8haEXxYw"; ud_cache_language=en; ud_cache_logged_in=1; ud_cache_marketplace_country=GB; ud_cache_user=74772298; ud_cache_release=a85dfa034e7cf489378d959d3d0a5b582e96801c; _pxhd=d43f8e35203d4cf2bc3c9c6acee34020fe09020b9ddcf8c366d133682095c3bf:80ff45b1-01ab-11ea-9518-8709089f635e; __cfruid=d12fc5432f56d3d1c0ee4bfc874f26ef9f740594-1585755153; _gid=GA1.2.2116444046.1585755246; IR_gbd=udemy.com; IR_5420=1585848740300%7Cc-8468%7C1585848671099%7C%7C; _ym_isad=2; quality_general=720; caption=; ud_credit_unseen=0; seen=1; eventing_session_id=ExRnMZCKRpCrYcJcJJZJWg-1585850536668; _ym_visorc_53931514=b; _gat=1; _gat_UA-12366301-1=1'
    cook_S = ck(c)
    cook_D = {}
    for key, morsel in cook_S.items():
        cook_D[key] = morsel.value
    pprint.pprint(cook_D)
    
    # SCARICA LA PAGINA INVIANDO LE COOKIES
    page = "https://www.udemy.com/"
    u = requests.get(page, cookies = cook_D)
    u.cookies.save()
    t = u.text 
    h0 = u.headers
    h = dict(h0)
    cj0 = u.cookies
    cj = cj0
    print('\n')
    pprint.pprint(h)
    print('\n')
    pprint.pprint(cj)
    print("PROGRAMMA TERMINATO")
    
else:    
    page = "https://www.tesco.com/groceries/en-GB/slots/delivery"
    cookies_T = "trkid=3f99fda4-2f71-4c23-95b5-2550fbf2d972; atrc=c54d4605-3201-41d5-8678-807f5e5658b7; h-e=0ab87a633b04141c9dd61b9546c44349a198a9d0914b17963565a369dce95929; cookiesAccepted=1584296666851; consumer=default; DCO=wdc; ighs-sess=eyJwYXNzcG9ydCI6eyJ1c2VyIjp7ImlkIjoiMTNmMzRhYzEtNDc0OS00MzgzLWExZTEtNTBkOWJkNWEyMTk2In19LCJzdG9yZUlkIjoiMzMyNCIsImFuYWx5dGljc1Nlc3Npb25JZCI6IjlmZTM4MWRkZDRjNTIyZmVhMjkyNDdiMDdmZTRmOGYwIn0=; ighs-sess.sig=bAz2st6vCVboWLZ7bbSwIPordII; itemsPerPage=24; waitingRoom=%7B%22key%22%3A%2220170825001%22%2C%22access%22%3A%22GRANTED%22%2C%22granted%22%3A1585845988%2C%22ttl%22%3A1585846048225%2C%22uuid%22%3A%221585845886400-7345213%22%2C%22hash%22%3A%22b3d02134%22%2C%22queueingSince%22%3A1585845886486%7D; atrc=c54d4605-3201-41d5-8678-807f5e5658b7; _abck=205D43C83190CA72CF3B5D5CF1DF371E~0~YAAQFQ8DFykV6cJwAQAA10lt3wOm0k4W/c3KnXOwzUQZAss9TdZE+pltOedBCw1ZYAJA1vMjK6HvmZdklpZvsbHvkvGvTsZjS2tIJvyLAweMeg5pMoxoxZ8iEo/6vYhs9kHPPjNOcTNQu6VFZ2rSUdp1ZV8VE2DwVcu5pfVHAHQKC3bjOSDZ/BXxbXPJ2OVJ0v0JEIHxi8impTjFRP5yACaIfIQZqzuVsDflkTNh49HQUiRpJacNHWxa5Jr4rSk62iThjMi2lBQXzgqe4efYI7QgVisFTSTWD8ifjCTQigmS9i1GgVA7jPhHTXCD2lhX03zRl2Fy~-1~-1~-1; AMCV_E4860C0F53CE56C40A490D45%40AdobeOrg=-1712354808%7CMCIDTS%7C18354%7CMCMID%7C34022507114548101124614441961596193192%7CMCAID%7C2F3738FF0515D2C6-60000A84059909A7%7CMCOPTOUT-1585853172s%7CNONE%7CMCAAMLH-1586450772%7C6%7CMCAAMB-1586450772%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C4.3.0%7CMCSYNCSOP%7C411-18359; s_vi=[CS]v1|2F3738FF0515D2C6-60000A84059909A7[CE]; s_ecid=MCMID%7C34022507114548101124614441961596193192; s_nr=1585845972642-Repeat; _ga=GA1.2.1721522818.1584296627; __gads=ID=6a49320174b03992:T=1584296555:S=ALNI_MZNm8ENgymucZ8-3eOcU_CpkrD4zQ; __sonar=17185570176616520030; _gcl_au=1.1.1505187641.1584296669; _fbp=fb.1.1584296669374.911138877; _4c_=jVPLbtswEPyVgIecIonLNw0EhfNw0AJJkD7QoyGJTCxYsQxRtuIG%2FvcsbdkNmqKoLtIuZ0e7s8NX0s%2F8goxAGmmEAqAC9BmZ%2B00go1fSVi6%2B1mRE8sJoK%2FVjYkvvElFwlRhjVUKFy7k1Ra65JGfkJXJZRjVTygJV2zNSLgeOV7Jqa6Sadd0yjLKs7%2Fu086Fs0rJ5zp7apvRt5UPmF8nNRRbqpguZ83W19u0GqcvGeawGm9qUY9z9wkhR%2FFq2jVuV3bTbLCOi98VJcHM8cH5dlX7aV66bxVLJ1e%2FszFdPsw7TRomYXbYRkrI4Rl8tXNP%2FWThkj4Xcxj6Wdb7pfR0nu8OwaJs%2B%2BMg1qVr%2F2Lyc6EjfoKDk544gYIgnvm13MIxC1cXGj2IMKVzDIeuQq%2ByS1TxpFsvWR8T97fev04vr8eX93TtRw7Pv2qoM75QtshCyXbiaH1WOmmWQffmWsBR0SpMr%2FXCXBbBaWg7cKA1afho%2FXJzD6XPlzrmgjEmqAYQUBigAQ78IIcAq3LgCrLLsNEcom3DNzWRCJcgrdqkSRfEZG0GltdSO9en44foconTRWSKusG7KvI4aoBtxeJy1atCXZN9vXP%2FNePrj81VchmYgGTNgUrStYFYppg963F7uMP%2FXLdkOhjU4c4QzMOirDleJnohN0%2B2%2ByZ1%2FBf0AVx%2Fh%2B%2F0Pff%2Br9m%2B%2Fqgc4HNF4K61AOfmAxiEO6HV1uJw%2Bh7wshUgkdSIRueNJwVmZFIJJcGC9YYy8o9QWpbGHBsDsGbfbNw%3D%3D; cookiesAccepted=1585846017525; updatedCookiesAccepted=1; _csrf=Jt1RbNqpkbo8g67s1Tk4Cs92; AMCVS_E4860C0F53CE56C40A490D45%40AdobeOrg=1; _gid=GA1.2.1773623775.1585778907; s_cc=true; s_sq=tescointgroceriesdev%3D%2526c.%2526a.%2526activitymap.%2526page%253Dhttps%25253A%25252F%25252Fwww.tesco.com%25252Fgroceries%25252Fen-GB%25252Fslots%2526link%253DHome%252520delivery%252520Your%252520online%252520shopping%252520delivered%252520to%252520your%252520fridge%252520door%252520seven%252520days%252520a%252520week%25255E%2526region%253Dmain%2526.activitymap%2526.a%2526.c; ADRUM=s=1585846110416&r=https%3A%2F%2Fwww.tesco.com%2Fgroceries%2Fen-GB%2Fslots%2Fdelivery%3F0; mytesco_from=https%3A%2F%2Fwww.tesco.com%2Fgroceries%2Fen-GB%2Fslots%2Fdelivery; akavpau_tesco_groceries=1585846317~id=782a8f24f4d293d68e2593f109e654a5; s_fid=4898B91341D310CF-361FF9B31D12325F; bm_sz=C8257971093E951DBA3EBC319173BA0E~YAAQa0dnaF49ejRxAQAAjdD6Ogdu8PQ4NfjhKkZCIoXZ3Xhe282a6R23d71Vq2MoX9EV+bYk/+uOMwunkTXeCcKDzhqh5eaDKaFTFtFp88Hl32bhg+3Ba7OQV6WVzPRTh7sfkrxQudFW9MYANbW1eXNoDSCFu+1TZiATAfqiEIWWh8AtZvROofWfZXLlR8M=; DCACC=AWS1; s_gpv_pn=login; OAuth.AccessToken=13f34ac1-4749-4383-a1e1-50d9bd5a2196; OAuth.TokensExpiryTime=%7B%22AccessToken%22%3A1585849485863%2C%22RefreshToken%22%3A1585853085863%7D; UUID=9464c104-de6a-4dbc-8b55-1dbb560dfd6e; CID=117449061; trm=taniboqGVou0f9Y2V5nk8BJemPSfZzaeu1UBi8vGNKARovcJCAFpR%2BBhcodHUPS6X4Qd0as%2BD5XD8IqFjw02rOJiXUj9FD%2BjU%2BrE8J%2FmjjintASXSpoRuhOykyZSsWZ9ygh%2B65RT3ACKjg%2BlcBFKoQIT3ZHQh3DjWFS76LBTCBOduSoYriCYgJFU506U2Lr5Pkvk2%2BUv; s_prevpage=slots%3Adelivery; _gat_ukLego=1"
    output_file = 'TESCO_orari_aggiornamento_Slot' + str(dt.date.today()) + '.txt'
    x = True

    while (x == True ):
        w = requests.get(page, cookies)
        p = w.text
        tree = html.fromstring(p)
        
        trova_riga_orari()

        try:
            f = open(output_file, 'a')
        except:
            print("file: ",output_file,"errore in apertura del file") 
        scrive_riga_orari()
        f.close
        time.sleep(1800)     

    print("programma terminato / premi un tasto per uscire. Orari salvati su file")
    x = input()
