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

########계좌번호#################### 
        self.account = 5624118510
#####################################


########변수####################     
        # 공통
        self.time_count = 0
        self.bid_price = {}
        self.ask_price = {}

        # algo_1
        self.spread_1 = []
        # algo_2 
        self.spread_2 = []
        # algo_3 
        self.spread_3 = []
        # algo_4 
        self.spread_4 = []
#################################


########종목코드 실시간 등록##############
        self.codes_one = ['A005930','A005935']
        # codes_three = ';123310'
        code_five = '005930;005935'
        code_six = '069500;114800;364690;365040'
        codes = code_five + ';' + code_six
        self.kiwoom.subscribe_stock_conclusion('2000',codes)
############################################


############종목수량, 매수/매도호가 #############
    def get_data(self):
        self.kiwoom.get_amount()
        bid_price = self.kiwoom.bid_price
        ask_price = self.kiwoom.ask_price
        # earning = self.kiwoom.earning
        return self.kiwoom.amount,bid_price, ask_price

    def get_price(self):
        import win32com.client
        # 연결 여부 체크
        objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        bConnect = objCpCybos.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            exit()
        # 현재가 객체 구하기
        objStockMst = win32com.client.Dispatch("DsCbo1.StockMst")
        # 현재가 정보 조회
        for code in self.codes_one:

            objStockMst.SetInputValue(0, code)   
            objStockMst.BlockRequest()

            # 현재가 통신 및 통신 에러 처리 
            rqStatus = objStockMst.GetDibStatus()
            rqRet = objStockMst.GetDibMsg1()
            # print("통신상태", rqStatus, rqRet)
            if rqStatus != 0:
                exit()

            name = objStockMst.GetHeaderValue(1)
            bid = objStockMst.GetHeaderValue(16)
            ask = objStockMst.GetHeaderValue(17)
            print(bid,ask)
            self.bid_price[name] = int(bid)
            self.ask_price[name] = int(ask)
    
        # return bid_price, ask_price    
#################################################



########매수/매도 메소드###########################################################################################
 # self.kiwoom.send_order("send_order_req", "0101", account, order_type, code, num, price, hoga, "")    00:지정가, 03 :시장가
    def buy_dafualt(self,code,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, code, leverage, price, '00', "")   

    def sell_defualt(self,code,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, code, leverage, price, '00', "")   

    def buy_kodex(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 364690, leverage, price, '00', "")   
        
    def sell_kodex(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 364690, leverage, price, '00', "")
        
    def buy_tiger(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, 365040, leverage, price, '00', "")
        
    def sell_tiger(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, 365040, leverage, price, '00', "")
        
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

    def buy_samsung(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, '005930', leverage, price, '00', "")
        
    def sell_samsung(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, '005930', leverage, price, '00', "")

    def buy_samsung_wu(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, '005935', leverage, price, '00', "")
        
    def sell_samsung_wu(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, '005935', leverage, price, '00', "")
###################################################################################################################



### trading algorithms ###
################################################### Algo_0##########################################################
    def zero(self,amount,bid_price,ask_price):
            
        ### 알고리즘 요약
        # 1. 가지고 있는 모든 포지션의 손익이 +인 경우 일괄매도        

        ### initial condition ###
        kodex200 = 'KODEX 200'
        kodex_inv = 'KODEX 인버스'   

        ### sell if profit is plus ###
        if self.kiwoom.cash > 2000:
            self.sell_kodex200(0,amount[kodex200])
            self.sell_kodex_inv(0,amount[kodex_inv])
            time.sleep(5)
            self.buy_kodex200(0,amount[kodex200])
            self.buy_kodex_inv(0,amount[kodex_inv])


################################################### Algo_1##########################################################
    def one(self):
        print('[algo_one]-----------------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. kodex200과 kodex_inv의 매수호가(매도가격) 스프레드가 지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 해당 지정가로 주문, 만약 해당 지정가로 주문 실패시 
        # 4. 반대 포지션으로 청산
        
        ###초기 설정###
        leverage = 1       
        init_count = 25
        time_term = 2
        hedge_ratio = 1

        ###변수 설정###
        kodex200 = 'KODEX 200'
        kodex_inv = 'KODEX 인버스'      
        bid_ask_spread = 25

        ###스프레드 계산###
        if len(self.bid_price)!=2:
            pass
        else:               
            print('bid_price :',self.bid_price)
            bid_kodex200 = self.bid_price[kodex200]  # 매수가격
            bid_kodex_inv = self.bid_price[kodex_inv]
            ask_kodex200 = self.ask_price[kodex200]    #매도가격
            ask_kodex_inv = self.ask_price[kodex_inv]
            self.spread_1.append(bid_kodex200 - bid_kodex_inv*hedge_ratio)             
            
            if len(self.spread_1) <= 100:
                print(len(self.spread_1),'/100')


        ###이동평균 계산 후 트레이딩 시작###
        if len(self.spread_1)>=100:

            spread_1 = pd.Series(self.spread_1)

            threshold = spread_1.rolling(window=100,center=False).mean()

            print('spread_inv :',round(spread_1.iloc[-1],4), 'threshold :',round((threshold.iloc[-1]),4), '   ///',
                    round(spread_1.iloc[-1]-(threshold.iloc[-1]),4))

            # if self.time_count % time_term == 0:
            if spread_1.iloc[-1] > (threshold.iloc[-1]+bid_ask_spread):
                amount = self.get_amount()
                amount_kodex200 = amount[kodex200]
                amount_kodex_inv = amount[kodex_inv]

                if amount_kodex200 >=1:
                    print('short position')
                    self.sell_kodex200(0,leverage)
                    self.buy_kodex_inv(0,leverage*hedge_ratio)

            elif spread_1.iloc[-1] < (-threshold.iloc[-1]-bid_ask_spread)  :
                amount = self.get_amount()
                amount_kodex200 = amount[kodex200]
                amount_kodex_inv = amount[kodex_inv]

                if amount_kodex_inv >=1:
                    print('long position')
                    self.sell_kodex_inv(0,leverage*hedge_ratio)
                    self.buy_kodex200(0,leverage)                  
            # self.time_count += 1
            # print('time to trade : ',  time_term - (self.time_count)%time_term)
 
            # if (threshold.iloc[-1]-5) < spread_1.iloc[-1] < (threshold.iloc[-1]+5) :
            if abs(spread_1.iloc[-1]) < (threshold.iloc[-1]+5) :
                amount = self.get_amount()
                amount_kodex200 = amount[kodex200]
                amount_kodex_inv = amount[kodex_inv]
                print('close position')                    
                if amount_kodex200 < init_count :
                    self.sell_kodex_inv(0,(init_count-amount_kodex200)*hedge_ratio)
                    self.buy_kodex200(0,init_count-amount_kodex200)
                elif amount[kodex200] > init_count :
                    self.sell_kodex200(0,amount_kodex200-init_count)
                    self.buy_kodex_inv(0,(amount_kodex200-init_count)*hedge_ratio)
                        
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
                    self.buy_tiger200(0,amount[samsung]-init_count)


################################################### Algo_3##########################################################
    def three(self,amount,bid_price,ask_price):
        print('[algo_three]----------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. KODEX 인버스과 TIGER 인버스의 매수호가(매도가격) 스프레드가 지난 60개의 데이터 이동평균과 달라지는 경우,
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


################################################### Algo_4########################################################## 

    def four(self,amount,bid_price,ask_price):
        print('[algo_four]--------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. KODEX 코스닥150선물인버스과 TIGER 코스닥150선물인버스의 매수호가(매도가격) 스프레드가 
        #    지난 60개의 데이터 이동평균과 달라지는 경우,
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
                    self.sell_tiger_kosdaqinv(0,leverage)
                    self.buy_kodex_kosdaqinv(0,leverage*hedge_ratio)


                elif spread_4.iloc[-1] < (threshold.iloc[-1]-bid_ask_spread) and amount[kodex_kosdaqinv]>=1 :
                    print('long position')
                    self.sell_kodex_koskosdaqinv(0,leverage*hedge_ratio)
                    self.buy_tiger_koskosdaqinv(0,leverage)                  
            self.time_count += 1
            print('time to trade : ',  time_term - (self.time_count)%time_term)

 
            if abs(spread_4.iloc[-1]) < (threshold.iloc[-1]+5) :
                print('close position')                    
                if amount[kodex_kosdaqinv] > init_count :
                    self.sell_kodex_koskosdaqinv(0,(amount[kodex_kosdaqinv])-init_count)
                    self.buy_tiger_koskosdaqinv(0,(amount[kodex_kosdaqinv])*hedge_ratio-init_count)
                elif amount[kodex_kosdaqinv] < init_count :
                    self.sell_tiger_koskosdaqinv(0,init_count-amount[kodex_kosdaqinv])
                    self.buy_kodex_koskosdaqinv(0,(init_count-amount[kodex_kosdaqinv])*hedge_ratio)
                        
        else:
            pass


        print('')


################################################### Algo_5########################################################## 

    def five(self,amount, bid_price, ask_price):
        print('[algo_five]--------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. 삼성전자와 삼성전자우의 매수호가(매수가격) 스프레드가 
        #    지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산
        
        ###초기 설정###
        leverage = 1
        init_count = 10
        hedge_ratio_7 = 1
        hedge_ratio_8 = 1

        samsung = '삼성전자' 
        samsung_wu = '삼성전자우'
        bid_ask_spread = 400
 
        amount_samsung = amount[samsung]
        amount_samsung_wu = amount[samsung_wu]

        ###스프레드 계산###
        if '005935' in bid_price.keys() and '005930' in bid_price.keys():
            bid_samsung = bid_price['005930']  # 매수가격
            bid_samsung_wu = bid_price['005935']
            ask_samsung = ask_price['005930']    #매도가격
            ask_samsung_wu = ask_price['005935']
            self.spread_4.append(bid_samsung*hedge_ratio_7-bid_samsung_wu*hedge_ratio_8 )             
            
            if len(self.spread_4) <= 150:
                print(len(self.spread_4),'/150')


        ###이동평균 계산 후 트레이딩 시작###
        if len(self.spread_4)>=150:

            spread_4 = pd.Series(self.spread_4)
            threshold = spread_4.rolling(window=150,center=False).mean()

            print('spread :',round(spread_4.iloc[-1],4), 'threshold :',round((threshold.iloc[-1]),4), '   ///',
                    round(spread_4.iloc[-1]-(threshold.iloc[-1]),4))

            # if self.time_count % time_term == 0:
            if spread_4.iloc[-1] > (threshold.iloc[-1]+bid_ask_spread):

                if amount_samsung_wu >=1:
                    print('short position')
                    self.sell_samsung_wu(ask_samsung_wu,leverage*hedge_ratio_8)
                    self.buy_samsung(bid_samsung,leverage*hedge_ratio_7)

            elif spread_4.iloc[-1] < (threshold.iloc[-1]-bid_ask_spread)  :

                if amount_samsung >=1:
                    print('long position')
                    self.sell_samsung(ask_samsung,leverage*hedge_ratio_7)
                    self.buy_samsung_wu(bid_samsung_wu,leverage*hedge_ratio_8)                  
            # self.time_count += 1
            # print('time to trade : ',  time_term - (self.time_count)%time_term)
 
            # if (threshold.iloc[-1]-5) < spread_1.iloc[-1] < (threshold.iloc[-1]+5) :
            if (threshold.iloc[-1]-100)< spread_4.iloc[-1] < (threshold.iloc[-1]+100) :
                print('close position')                    
                if amount_samsung < init_count :
                    self.sell_samsung_wu(ask_samsung_wu,(init_count-amount_samsung))
                    self.buy_samsung(bid_samsung,(init_count-amount_samsung))
                elif amount[samsung] > init_count :
                    self.sell_samsung(ask_samsung,(amount_samsung-init_count))
                    self.buy_samsung_wu(bid_samsung_wu,(amount_samsung-init_count))
                        
        else:
            pass

        print('')


################################################### Algo_6########################################################## 

    def six(self,amount, bid_price, ask_price):
        print('[algo_six]--------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. 삼성전자와 삼성전자우의 매수호가(매수가격) 스프레드가 
        #    지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산
        
        ###초기 설정###
        leverage = 1
        init_count = 30

        kodex_active = 'KODEX 혁신기술테마액티브' 
        tiger_active = 'TIGER AI코리아그로스액티브'

        if kodex_active in amount.keys():
            amount_kodex_active = amount[kodex_active]
        else:
            amount_kodex_active = 0
            
        if tiger_active in amount.keys():
            amount_tiger_active = amount[tiger_active]
        else:
            amount_tiger_active = 0


        ### get bid ask###
        if '364690' in bid_price.keys() and '365040' in bid_price.keys():            
            bid_kodex_active = bid_price['364690']  # 매수가격
            bid_tiger_active = bid_price['365040']
            ask_kodex_active = ask_price['364690']  # 매도가격
            ask_tiger_active = ask_price['365040']


            if ask_kodex_active > bid_tiger_active and amount_tiger_active<=59:  
                print('short position')   
                self.sell_kodex(ask_kodex_active,leverage)
                self.buy_tiger(bid_tiger_active,leverage)

            elif ask_tiger_active > bid_kodex_active and amount_tiger_active<=59 :
                print('long position')   
                self.sell_tiger(ask_tiger_active,leverage)
                self.buy_kodex(bid_kodex_active,leverage)                  


            if amount_kodex_active > init_count and  ask_kodex_active == bid_tiger_active:
                print('close position')                    
                self.sell_kodex(ask_kodex_active,(amount_kodex_active-init_count))
                self.buy_tiger(bid_tiger_active,(amount_kodex_active-init_count))
            elif amount_tiger_active > init_count and  bid_kodex_active == ask_tiger_active :
                print('close position')
                self.sell_tiger(bid_kodex_active,(amount_tiger_active-init_count))
                self.buy_kodex(ask_tiger_active,(amount_tiger_active-init_count))
                    

        print('')
