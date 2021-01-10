import pandas as pd
import html
from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome('C:/Users/chhch/chromedriver_win32/chromedriver.exe')

####### load ETF codes excel ######
codes = pd.read_pickle('C:/Users/chhch/algorithmtrading/PyTrader_KIWOOM/active_etf/etf_components/ETF_Codes')
code_to_name = {}
for i in range(len(codes)):
    code_to_name[codes['code'].iloc[i]] = list(codes.index)[i]
###################################################################


###### get bid & ask price of each ETF #####################
five_spread = []
ten_spread = []

for code in codes['code']:
    url = 'https://finance.daum.net/quotes/A'+code+'#current/quote'
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    try:
        bid = soup.select('.downBox > .num')[-1].text  ; bid = int(bid.replace(',',''))
        ask = soup.select('.upBox > .num')[0].text     ; ask = int(ask.replace(',',''))
    except:
        pass
    # print(code_to_name[code],bid,ask)
    if bid - ask == 5:
        five_spread.append(code)
        print(code_to_name[code])
    if bid - ask == 10:
        ten_spread.append(code)
        # print(code_to_name[code])