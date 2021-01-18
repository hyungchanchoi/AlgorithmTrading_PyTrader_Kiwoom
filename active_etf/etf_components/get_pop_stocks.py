import pandas as pd
import html
from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome('C:/Users/chhch/chromedriver_win32/chromedriver.exe')


etf = ['naver','kodex','tiger']
url = ['https://finance.naver.com/sise/lastsearch2.nhn',
       'https://wisefn.finance.daum.net/v1/ETF/index.aspx?cmp_cd=364690',
       'https://wisefn.finance.daum.net/v1/ETF/index.aspx?cmp_cd=365040']

###### get pop stocks #####################



url = 'https://finance.naver.com/sise/lastsearch2.nhn'
driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

name = soup.select('contentarea > div.box_type_l > table > tbody > tr:nth-child(3) > td:nth-child(2) > a > .title')  
# prop = soup.select('.upBox > .num')[0].text     ; ask = int(ask.replace(',',''))       
# prop = soup.select('.upBox > .num')[0].text     ; ask = int(ask.replace(',',''))  
# prop = soup.select('.upBox > .num')[0].text     ; ask = int(ask.replace(',',''))  
# prop = soup.select('.upBox > .num')[0].text     ; ask = int(ask.replace(',',''))  
print(name)


#contentarea > div.box_type_l > table > tbody > tr:nth-child(3) > td:nth-child(2) > a
# five_spread = pd.DataFrame(five_spread)
# five_spread.to_excel('C:/Users/chhch/algorithmtrading/PyTrader_KIWOOM/active_etf/etf_components/ETF_Codes/five_spread')
