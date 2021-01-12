import pandas as pd
import numpy as np
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *
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

########계좌번호######## 
        self.account = 5624118510
#############################################################


########변수########
        
        # 공통
        self.time_count = 0
        # algo_1
        self.spread_1 = []
        # algo_2 
        self.spread_2 = []
        # algo_3 
        self.spread_3 = []
        # algo_4 
        self.spread_4 = []

#############################################################
        

########종목코드 실시간 등록########
        self.codes = '123310;114800;251340;250780'
        self.kiwoom.subscribe_stock_conclusion('2000', self.codes)
##############################################################


############종목수량, 매수/매도호가 ##########################
    def get_data(self):
        self.kiwoom.get_amount()
        amount = self.kiwoom.amount 
        bid_price = self.kiwoom.bid_price
        ask_price = self.kiwoom.ask_price
        return amount , bid_price, ask_price
###############################################################################################



########매수/매도 메소드###########################################################################################
 # self.kiwoom.send_order("send_order_req", "0101", account, order_type, code, num, price, hoga, "")    00:지정가, 03 :시장가

    def buy_kodex(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 364690, leverage, price, '03', "")   
        
    def sell_kodex(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 364690, leverage, price, '03', "")
        
    def buy_tiger(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 365040, leverage, price, '03', "")
        
    def sell_tiger(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 365040, leverage, price, '03', "")
        
    def buy_kodex200(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, '069500', leverage, price, '03', "")
        
    def sell_kodex200(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, '069500', leverage, price, '03', "")

    def buy_tiger200(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, '102110', leverage, price, '03', "")
        
    def sell_tiger200(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, '102110', leverage, price, '03', "")
        
    def buy_kodex_inv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 114800, leverage, price, '03', "")
        
    def sell_kodex_inv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 114800, leverage, price, '03', "")

    def buy_tiger_inv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 123310, leverage, price, '03', "")
        
    def sell_tiger_inv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 123310, leverage, price, '03', "")

    def buy_kodex_kosdaqinv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 251340, leverage, price, '03', "")
        
    def sell_kodex_kosdaqinv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 251340, leverage, price, '03', "")

    def buy_tiger_kosdaqinv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 250780, leverage, price, '03', "")
        
    def sell_tiger_kosdaqinv(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 250780, leverage, price, '03', "")
###################################################################################################################



### trading algorithms ###
################################################### Algo_1##########################################################
    def one(self,amount,bid_price,ask_price):
        print('[algo_one]-----------------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. kodex200과 kodex_inv의 매수호가(매도가격) 스프레드가 지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산
        
        ###초기 설정###
        leverage = 1       
        init_count = 30
        time_term = 2
        hedge_ratio = 11

        kodex200 = 'KODEX 200'
        kodex_inv = 'KODEX 인버스'      
        bid_ask_spread = 30

        ###스프레드 계산###
        if len(bid_price)!=2:
            pass
        else:               
            print(bid_price['069500'],bid_price['114800'],hedge_ratio)
            self.spread_1.append(bid_price['069500']-bid_price['114800']*hedge_ratio)             
            
            if len(self.spread_1) <= 60:
                print(len(self.spread_1),'/60')


        ###이동평균 계산 후 트레이딩 시작###
        if len(self.spread_1)>=60:
 
            spspread_1read_inv = pd.Series(self.spread_1)

            threshold = spread_1.rolling(window=60,center=False).mean()

            print('spread_inv :',round(spread_1.iloc[-1],4), 'threshold :',round((threshold.iloc[-1]),4), '/',
                    round(spread_inv.iloc[-1]-(threshold.iloc[-1]),4))

            if self.time_count % time_term == 0:
                if spread_inv.iloc[-1] > (threshold.iloc[-1]+bid_ask_spread) and amount[kodex200] >=1:
                    print('short position')
                    self.sell_kodex200(0,leverage)
                    self.buy_kodex_inv(0,leverage*hedge_ratio)


                elif spread_inv.iloc[-1] < (threshold.iloc[-1]-bid_ask_spread) and amount[kodex_inv]>=1 :
                    print('long position')
                    self.sell_kodex_inv(0,leverage*hedge_ratio)
                    self.buy_kodex200(0,leverage)                  
            self.time_count += 1
            print('time to trade : ',  time_term - (self.time_count)%time_term)

 
            if (threshold.iloc[-1]-5)  < spread_inv.iloc[-1] < (threshold.iloc[-1]+5) :
                print('close position')                    
                if amount[kodex200] < init_count :
                    self.sell_kodex_inv(0,(init_count-amount[kodex200])*hedge_ratio)
                    self.buy_kodex200(0,init_count-amount[kodex200])
                elif amount[kodex200] > init_count :
                    self.sell_kodex200(0,amount[kodex200]-init_count)
                    self.buy_kodex_inv(0,(amount[kodex200]-init_count)*hedge_ratio)
                        
        else:
            pass


        print('------------------------------------------------------------------------------')


################################################### Algo_2##########################################################
    def two(self,amount,bid_price,ask_price):
        print('[algo_two]-----------------------------------------------------------------------------')
        
        ### 알고리즘 요약
        # 1. kodex200과 tiger200의 매도가격 스프레드가 지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산


        ###초기 설정###
        leverage = 1       
        init_count = 20
        bid_ask_spread = 15

        kodex200 = 'KODEX 200'   
        tiger200 = 'TIGER 200'     
        

        ######스프레드 계산######
        if len(bid_price)!=3:
            pass
        else:    
            self.spread.append(bid_price['069500']-bid_price['102110'])  
            if len(self.spread) <= 60:
                print(len(self.spread),'/60')


        ######이동평균 계산 후 트레이딩 시작######
        if len(self.spread)>=60:
 
            spread = pd.Series(self.spread)

            threshold = spread.rolling(window=60,center=False).mean()

            print('spread :',round(spread.iloc[-1],4), 'threshold :',round((threshold.iloc[-1]+bid_ask_spread),4))

            if spread.iloc[-1] > (threshold.iloc[-1]+bid_ask_spread) and amount[kodex200] >=1:
                print('short position')
                self.sell_kodex200(0,leverage)
                self.buy_tiger200(0,leverage)

            elif spread.iloc[-1] < - (threshold.iloc[-1]+bid_ask_spread) and amount[tiger200]>=1 :
                print('long position')
                self.buy_kodex200(0,leverage)
                self.sell_tiger200(0,leverage)

            elif abs(spread.iloc[-1]) <= threshold.iloc[-1] :
                print('close position')                    
                if amount[kodex200] < init_count :
                    self.buy_kodex200(0,init_count-amount[kodex200])
                    self.sell_tiger200(0,init_count-amount[kodex200])
                elif amount[kodex200] > init_count :
                    self.sell_kodex200(0,amount[kodex200]-init_count)
                    self.buy_tiger200(0,amount[kodex200]-init_count)


################################################### Algo_3##########################################################
    def three(self,amount,bid_price,ask_price):
        print('[algo_three]----------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. kodex200과 kodex_inv의 매수호가(매도가격) 스프레드가 지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산
        
        ###초기 설정###
        leverage = 5
        init_count = 75
        time_term = 1
        hedge_ratio = 1

        kodex_inv = 'KODEX 인버스' 
        tiger_inv = 'TIGER 인버스'
        bid_ask_spread = 20

        ###스프레드 계산###
        if '114800' in bid_price.keys() and '123310' in bid_price.keys():              
            print(bid_price)
            self.spread_3.append(bid_price['123310']-bid_price['114800']*hedge_ratio)             
            
            if len(self.spread_3) <= 60:
                print(len(self.spread_3),'/60')


        ###이동평균 계산 후 트레이딩 시작###
        if len(self.spread_3)>=60:
 
            spread_3 = pd.Series(self.spread_3)

            threshold = spread_3.rolling(window=60,center=False).mean()

            print('spread_3 :',round(spread_3.iloc[-1],4), 'threshold :',round((threshold.iloc[-1]),4), '/',
                    round(spread_3.iloc[-1]-(threshold.iloc[-1]),4))

            if self.time_count % time_term == 0:
                if spread_3.iloc[-1] > (threshold.iloc[-1]+bid_ask_spread) and amount[kodex_inv] >=1:
                    print('short position')
                    self.sell_tiger_inv(0,leverage)
                    self.buy_kodex_inv(0,leverage*hedge_ratio)


                elif spread_3.iloc[-1] < (threshold.iloc[-1]-bid_ask_spread) and amount[tiger_inv]>=1 :
                    print('long position')
                    self.sell_kodex_inv(0,leverage*hedge_ratio)
                    self.buy_tiger_inv(0,leverage)                  
            self.time_count += 1
            print('time to trade : ',  time_term - (self.time_count)%time_term)

 
            if abs(spread_3.iloc[-1]) < (threshold.iloc[-1]+5) :
                print('close position')                    
                if amount[kodex_inv] > init_count :
                    self.sell_kodex_inv(0,amount[kodex_inv]-init_count)
                    self.buy_tiger_inv(0,(amount[kodex_inv]-init_count)*hedge_ratio)
                elif amount[kodex_inv] < init_count :
                    self.sell_tiger_inv(0,(init_count-amount[kodex_inv])*hedge_ratio)
                    self.buy_kodex_inv(0,init_count-amount[kodex_inv])

        else:
            pass


        print('------------------------------------------------------------------------------')


################################################### Algo_4##########################################################
    def four(self,amount,bid_price,ask_price):
        print('[algo_four]--------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. kodex200과 kodex_inv의 매수호가(매도가격) 스프레드가 지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산
        
        ###초기 설정###
        leverage = 5
        init_count = 75
        time_term = 1
        hedge_ratio = 1

        kodex_kosdaqinv = 'KODEX 코스닥150선물인버스' 
        tiger_kosdaqinv = 'TIGER 코스닥150선물인버스'
        bid_ask_spread = 20

        ###스프레드 계산###
        if '251340' in bid_price.keys() and '250780' in bid_price.keys() :      
            print(bid_price)
            self.spread_4.append(bid_price['250780']-bid_price['251340']*hedge_ratio)             
            
            if len(self.spread_4) <= 60:
                print(len(self.spread_4),'/60')


        ###이동평균 계산 후 트레이딩 시작###
        if len(self.spread_4)>=60:
 
            spread_4 = pd.Series(self.spread_4)

            threshold = spread_4.rolling(window=60,center=False).mean()

            print('spread_4 :',round(spread_4.iloc[-1],4), 'threshold :',round((threshold.iloc[-1]),4), '/',
                    round(spread_4.iloc[-1]-(threshold.iloc[-1]),4))

            if self.time_count % time_term == 0:
                if spread_4.iloc[-1] > (threshold.iloc[-1]+bid_ask_spread) and amount[tiger_kosdaqinv] >=1:
                    print('short position')
                    self.sell_tiger_kosadqinv(0,leverage)
                    self.buy_kodex_kosadqinv(0,leverage*hedge_ratio)


                elif spread_4.iloc[-1] < (threshold.iloc[-1]-bid_ask_spread) and amount[kodex_kosdaqinv]>=1 :
                    print('long position')
                    self.sell_kodex_kosadqinv(0,leverage*hedge_ratio)
                    self.buy_tiger_kosadqinv(0,leverage)                  
            self.time_count += 1
            print('time to trade : ',  time_term - (self.time_count)%time_term)

 
            if abs(spread_4.iloc[-1]) < (threshold.iloc[-1]+5) :
                print('close position')                    
                if amount[kodex_kosdaqinv] > init_count :
                    self.sell_kodex_kosadqinv(0,(amount[kodex_kosdaqinv])-init_count)
                    self.buy_tiger_kosadqinv(0,(amount[kodex_kosdaqinv])*hedge_ratio-init_count)
                elif amount[kodex_kosdaqinv] < init_count :
                    self.sell_tiger_kosadqinv(0,init_count-amount[kodex_kosdaqinv])
                    self.buy_kodex_kosadqinv(0,(init_count-amount[kodex_kosdaqinv])*hedge_ratio)
                        
        else:
            pass


        print('------------------------------------------------------------------------------')