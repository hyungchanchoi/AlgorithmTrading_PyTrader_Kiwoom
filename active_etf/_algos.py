
# coding: utf-8

# # Tools

# In[1]:
import pandas as pd
import numpy as np

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from _Kiwoom import *
import time
from datetime import datetime,timedelta
now = datetime.now()

form_class = uic.loadUiType("_pytrader.ui")[0]

class Algos(QMainWindow, form_class):

    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
        self.trade_stocks_done = False                
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()
        
        self.account = 5624118510
        self.leverage = 1

        self.kodex_cumret = [] ; self.tiger_cumret = [] 
        self.kodex_kospi = [] ; self.tiger_kospi = [] 

#       self.kiwoom.send_order("send_order_req", "0101", account, order_type, code, num, price, hoga, "")    00:지정가, 03 :시장가
    def buy_kodex(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, 364690, leverage, price, '03', "")
        
    def sell_kodex(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, 364690, leverage, price, '03', "")
        
    def buy_tiger(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, 365040, leverage, price, '03', "")
        
    def sell_tiger(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, 365040, leverage, price, '03', "")
        
    def buy_kospi(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, '069500', leverage, price, '00', "")
        
    def sell_kospi(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, '069500', leverage, price, '00', "")
        
    def buy_inverse(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, 114800, leverage, price, '03', "")
        
    def sell_inverse(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, 114800, leverage, price, '03', "")

################################################### Algo_1##########################################################
    def one(self):
    
        leverage = 1

        count_tiger = 40  #초기 종목 개수
        count_kodex = 40

        kodex = 'KODEX 혁신기술테마액티브'
        tiger = 'TIGER AI코리아그로스액티브'        
        codes = ['364690','365040'] ; self.kiwoom.codes = codes

        amount = self.kiwoom.amount
        print(amount)        
        for code in codes:
            self.kiwoom.get_real_data(code)
        
        price = self.kiwoom.price
        ret = self.kiwoom.rate
        print(price)
        print(ret)
        
        if len(price)!=3:
            pass
        else:
            kodex_price=price['364690'] ; tiger_price=price['365040']           
            self.kodex_tiger.append(kodex_price/10005 - tiger_price/10085 ) 
            print(len(self.kodex_tiger),'/100')

        if len(self.kodex_tiger)>100:
            del self.kodex_tiger[0]
            cumret_spread = pd.Series(self.kodex_tiger)
            threshold = cumret_spread.rolling(window=100,center=False).mean()
            
            if cumret_spread.iloc[-1] > threshold.iloc[-1]:
                print(round(cumret_spread.iloc[-1],4))
                self.sell_kodex(kodex_price,leverage)
                self.buy_tiger(tiger_price,leverage)
            elif cumret_spread.iloc[-1] < - threshold.iloc[-1]:
                print(round(cumret_spread.iloc[-1],4))
                self.buy_kodex(kodex_price,leverage)
                self.sell_tiger(tiger_price,leverage)
            elif abs(cumret_spread.iloc[-1]) < threshold.iloc[-1]*0.8:
                print(round(cumret_spread.iloc[-1],4))
                try:
                    if amount[kodex] < count_kodex:
                        self.buy_kodex(kodex_price,count_kodex-amount[kodex])
                        self.sell_tiger(tiger_price,count_kodex-amount[kodex])
                    elif amount[kodex] > count_kodex:
                        self.sell_kodex(kodex_price,amount[kodex]-count_kodex)
                        self.buy_tiger(tiger_price,amount[kodex]-count_kodex)
                except:
                    pass
            else:
                pass
        
    print('------------------------------------------------------------------------------')
################################################### Algo_2##########################################################
    def two(self):
    
        leverage = 1

        count_kodex = 30  #초기 종목 개수
        count_tiger = 30
        count_kospi = 180
        

        kospi = 'KODEX 인버스                '
        kodex = 'KODEX 혁신기술테마액티브                '
        tiger = 'TIGER AI코리아그로스액티브                '        
        codes = ['114800','364690','365040'] ; self.kiwoom.codes = codes

        amount = self.kiwoom.amount
        print(amount)   

        for code in codes:
            self.kiwoom.get_real_data(code)
        
        price = self.kiwoom.price
        ret = self.kiwoom.rate
        print(price)
        print(ret)
        
        if len(price)!=3:
            pass
        else:
            kospi_price=price['114800'] ; kodex_price=price['364690'] ; tiger_price=price['365040']
            kospi_ret=(kospi_price-5485)/5485 ; kodex_ret=(kodex_price-10005)/10005 ; tiger_ret=(tiger_price-10085)/10085

            self.kodex_kospi.append(kodex_ret - kospi_ret)
            self.tiger_kospi.append(tiger_ret - kospi_ret)

            if len(self.kodex_kospi) <=100:
                print(len(self.kodex_kospi),'/100') 
        
        if len(self.kodex_kospi)>100:

            kodex_kospi = pd.Series(self.kodex_kospi)
            threshold_kodex = kodex_kospi.rolling(window=100,center=False).mean()
            print('kodex :',round(kodex_kospi.iloc[-1],4) , round(threshold_kodex.iloc[-1],4))

            if kodex_kospi.iloc[-1] > threshold_kodex.iloc[-1]:
                self.sell_kodex(kodex_price,leverage)
                self.buy_inverse(kospi_price,3*leverage)
            elif kodex_kospi.iloc[-1] < - threshold_kodex.iloc[-1]:
                self.buy_kodex(kodex_price,leverage)
                self.sell_inverse(kospi_price,3*leverage)
            elif abs(kodex_kospi.iloc[-1]) < threshold_kodex.iloc[-1]-0.0003 :
                try :
                    if amount[kodex] < count_kodex:
                        self.buy_kodex(kodex_price,count_kodex-amount[kodex])
                        self.sell_inverse(kospi_price,3*(count_kodex-amount[kodex]))
                    elif amount[kodex] > count_kodex:
                        self.sell_kodex(kodex_price,amount[kodex]-count_kodex)
                        self.buy_inverse(kospi_price,3*(amount[kodex]-count_kodex))
                except:
                    pass
            else:
                pass
        else:
            pass
        
        if len(self.tiger_kospi)>=100:

            tiger_kospi = pd.Series(self.tiger_kospi)           
            threshold_tiger = tiger_kospi.rolling(window=100,center=False).mean()
            print('tiger :',round(tiger_kospi.iloc[-1],4) , round(threshold_tiger.iloc[-1],4))
            
            if tiger_kospi.iloc[-1] > threshold_tiger.iloc[-1]:
                self.sell_tiger(tiger_price,leverage)
                self.buy_inverse(kospi_price,3*leverage)
            elif tiger_kospi.iloc[-1] < - threshold_tiger.iloc[-1]:    
                self.buy_tiger(tiger_price,leverage)
                self.sell_inverse(kospi_price,3*leverage)
            elif abs(tiger_kospi.iloc[-1]) < threshold_tiger.iloc[-1]-0.0003:
                try:
                    if amount[tiger] < count_tiger:
                        self.buy_tiger(tiger_price,count_tiger-amount[tiger])
                        self.sell_inverse(kospi_price,3*(count_tiger-amount[tiger]))
                    elif amount[tiger] > count_tiger:
                        self.sell_tiger(tiger_price,amount[tiger]-count_tiger)
                        self.buy_inverse(kospi_price,3*(amount[tiger]-count_tiger))
                except:
                    pass
            else:
                pass
    print('------------------------------------------------------------------------------')

################################################### Algo_3##########################################################
def three(self):
    
        leverage = 1

        count_kodex = 30  #초기 종목 개수
        count_tiger = 30
        count_kospi = 60

        kospi = 'KODEX 200'
        kodex = 'KODEX 혁신기술테마액티브'
        tiger = 'TIGER AI코리아그로스액티브'        
        codes = ['069500','364690','365040'] ; self.kiwoom.codes = codes

        amount = self.kiwoom.amount
        print(amount)        
        for code in codes:
            self.kiwoom.get_real_data(code)
        
        price = self.kiwoom.price
        ret = self.kiwoom.rate
        print(price)
        print(ret)
        
        if len(price)!=3:
            pass
        else:
            kospi_price=price['069500']; kodex_price=price['364690'] ; tiger_price=price['365040']
            kospi_ret=ret['069500']   ; kodex_ret=ret['364690']   ; tiger_ret=ret['365040']

            self.kodex_kospi.append(kodex_ret - kospi_ret)
            self.tiger_kospi.append(tiger_ret - kospi_ret)

        if len(self.kodex_kospi)>=60:
            
            kodex_kospi = pd.Series(self.kodex_kospi)
            threshold_kodex = kodex_kospi.rolling(window=100,center=False).mean()
            
            if kodex_kospi.iloc[-1] > threshold_kodex.iloc[-1]:
                print(round(kodex_kospi.iloc[-1],4))
                self.sell_kodex(kodex_price,leverage)
                self.buy_kospi(kospi_price,leverage)
            elif kodex_kospi.iloc[-1] < - threshold_kodex.iloc[-1]:
                print(round(kodex_kospi.iloc[-1],4))
                self.buy_kodex(kodex_price,leverage)
                self.sell_kospi(kospi_price,leverage)
            elif abs(kodex_kospi.iloc[-1]) < threshold_kodex.iloc[-1]:
                print(round(kodex_kospi.iloc[-1],4))
                if amount[kodex] < count_kodex:
                    self.buy_kodex(kodex_price,leverage)
                    self.sell_kospi(kospi_price,count_kodex-amount[kodex])
                elif amount[kodex] > count_kodex:
                    self.sell_kodex(kodex_price,leverage)
                    self.buy_inverse(kospi_price,amount[kodex]-count_kodex)
            else:
                pass
        else:
            pass
        
        if len(tiger_ret)>=60:
            
            tiger_kospi = pd.Series(tiger_kospi)           
            threshold_tiger = tiger_kospi.rolling(window=100,center=False).mean()
            
            if tiger_kospi.iloc[-1] > threshold_tiger.iloc[-1]:
                print(round(tiger_kospi.iloc[-1],4))
                self.sell_tiger(tiger_price,leverage)
                self.buy_kospi(kospi_price,leverage)
            elif tiger_kospi.iloc[-1] < - threshold_tiger.iloc[-1]:
                print(round(tiger_kospi.iloc[-1],4))
                self.buy_tiger(tiger_price,leverage)
                self.sell_kospi(kospi_price,leverage)
            elif abs(tiger_kospi.iloc[-1]) < threshold_tiger.iloc[-1]:
                print(round(tiger_kospi.iloc[-1],4))
                if amount[tiger] < count_tiger:
                    self.buy_tiger(tiger_price,leverage)
                    self.sell_kospi(kospi_price,count_tiger-amount[tiger])
                elif amount[tiger] > count_tiger:
                    self.sell_tiger(tiger_price,leverage)
                    self.buy_kospi(kospi_price,amount[tiger]-count_tiger)
            else:
                pass
print('------------------------------------------------------------------------------')