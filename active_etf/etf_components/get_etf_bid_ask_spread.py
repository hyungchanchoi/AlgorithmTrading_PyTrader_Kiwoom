from pykiwoom.kiwoom import *
import pandas as pd
from urllib.request import urlopen
import bs4
from datetime import datetime
today = datetime.today().strftime("%Y%m%d")


###### check connection with kiwoom api ######
kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
state = kiwoom.GetConnectState()
if state == 0:
    print("미연결")
elif state == 1:
    print("연결완료")
########################################################



###### save name and code as dictionary #######
name_to_code = {}
code_to_name = {}
etf = kiwoom.GetCodeListByMarket(8)

for code in etf:
    name = kiwoom.GetMasterCodeName(code)
    name_to_code[name] = code
    code_to_name[code] = name
########################################################


for code in etf[0]:
    url = 'https://finance.daum.net/quotes/A'+'091180'+'#current/quote'

    source = urlopen(url).read()
    source = bs4.BeautifulSoup(source, 'lxml')
    tag = source.find_all('span',class_='num')
    print(tag)