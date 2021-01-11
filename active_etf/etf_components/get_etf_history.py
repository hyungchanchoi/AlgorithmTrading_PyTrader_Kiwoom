import pandas as pd
from urllib.request import urlopen
import bs4
from datetime import datetime
today = datetime.today().strftime("%Y%m%d")

etf = ['kospi','kodex','tiger']
url = ['https://wisefn.finance.daum.net/v1/ETF/index.aspx?cmp_cd=069500',
       'https://wisefn.finance.daum.net/v1/ETF/index.aspx?cmp_cd=364690',
       'https://wisefn.finance.daum.net/v1/ETF/index.aspx?cmp_cd=365040']
with pd.ExcelWriter('C:/Users/chhch/algorithmtrading/PyTrader_KIWOOM/active_etf/etf_components/'+str(today)+'.xlsx') as writer:
    
    for j in range(len(etf)):
        source = urlopen(url[j]).read()
        source = bs4.BeautifulSoup(source, 'lxml')
        tag = source.find_all('td',class_='c1 txt ellipsis')

        name = []; num = []; per = []    

        for i in range(len(tag)):
            name.append(source.find_all('td', class_='c1 txt ellipsis')[i].text)
            num.append(source.find_all('td', class_='c2 num')[i].text)
            per.append(source.find_all('td', class_='c3 num')[i].text)

        temp = etf[j]
        temp = pd.DataFrame(index=range(0,len(name)), columns= ['name','num','per'])    
        temp['name']=name
        temp['num']=num
        temp['per']=per
        temp.to_excel(writer, sheet_name=etf[j])