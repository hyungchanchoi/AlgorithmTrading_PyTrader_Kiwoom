import pandas as pd
import html
from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome('C:/Users/chhch/chromedriver_win32/chromedriver.exe')

# ###### load ETF codes excel ######
codes = pd.read_pickle('C:/Users/chhch/algorithmtrading/PyTrader_KIWOOM/active_etf/etf_components/ETF_Codes')
# ########################################################


for code in codes['code'][0]:
    url = 'https://finance.daum.net/quotes/A'+'091180'+'#current/quote'
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    temp = soup.select('span.num')
    print(len(temp))
