
# coding: utf-8

# # Tools

# In[1]:


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

#       self.kiwoom.send_order("send_order_req", "0101", account, order_type, code, num, price, hoga, "")    
    def buy_kodex(self,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, 364690, leverage, 0, '03', "")
        
    def sell_kodex(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, 364690, leverage, price, '00', "")
        
    def buy_tiger(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, 365040, leverage, price, '00', "")
        
    def sell_tiger(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, 365040, leverage, price, '00', "")
        
    def buy_kospi(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, '069500', leverage, price, '00', "")
        
    def sell_kospi(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, '069500', leverage, price, '00', "")
        
    def buy_inverse(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 1, 114800, leverage, price, '00', "")
        
    def sell_inverse(self,price,leverage):
        self.kiwoom.send_order("send_order_req", "0101", self.account, 2, 114800, self.leverage, price, '00', "")


################################################### Algo_1##########################################################
    def one(self):

        leverage = 1

        count_kodex = 30
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
        rate = self.kiwoom.rate
        print(price)
        print(rate)

        kospi_price = [] ; kodex_price = [] ;tiger_price = [] 
        kospi_ret = [] ; kodex_ret = [] ;tiger_ret = [] 
        
        if len(price)!=3:
            pass
        else:
            kospi_price.append(price['069500']); kodex_price.append(price['364690']) ; tiger_price.append(price['365040'])
            kospi_ret.append(rate['069500'])   ; kodex_ret.append(rate['364690'])    ; tiger_ret.append(rate['365040'])

            kodex_kospi = kodex_ret[-1] - kospi_ret[-1]
            tiger_kospi = tiger_ret[-1] - kospi_ret[-1]

            if kodex_kospi > threshold_buy:
                print(round(kodex_kospi,4))
                self.sell_kodex(kodex_price,leverage)
                self.buy_kospi(kospi_price,leverage)
            elif kodex_kospi < - threshold_buy:
                print(round(kodex_kospi,4))
                self.buy_kodex(kodex_price,leverage)
                self.sell_kospi(kospi_price,leverage)
            elif abs(kodex_kospi) < threshold_sell:
                print(round(kodex_kospi,4))
                if amount[kodex] < count_kodex:
                    self.buy_kodex(kodex_price,leverage)
                    self.sell_kospi(kospi_price,count_kodex-amount[kodex])
                elif amount[kodex] > count_kodex:
                    self.sell_kodex(kodex_price,leverage)
                    self.buy_inverse(kospi_price,amount[kodex]-count_kodex)
            else:
                pass

            if tiger_kospi > threshold_buy:
                print(round(tiger_kospi,4))
                self.sell_tiger(tiger_price,leverage)
                self.buy_kospi(kospi_price,leverage)
            elif tiger_kospi < - threshold_buy:
                print(round(tiger_kospi,4))
                self.buy_tiger(tiger_price,leverage)
                self.sell_kospi(kospi_price,leverage)
            elif abs(tiger_kospi) < threshold_sell:
                print(round(tiger_kospi,4))
                if amount[tiger] < count_tiger:
                    self.buy_tiger(tiger_price,leverage)
                    self.sell_kospi(kospi_price,count_tiger-amount[tiger])
                elif amount[tiger] > count_tiger:
                    self.sell_tiger(tiger_price,leverage)
                    self.buy_kospi(kospi_price,amount[tiger]-count_tiger)
            else:
                pass
print('------------------------------------------------------------------------------')