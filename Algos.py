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
        self.check = True
        self.profit = 0
        self.amount = {}
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
        code_two = '069500;102110'
        code_five = '005930;005935'
        code_six = '364690;365040'
        codes = code_two # + ';' + code_five + ';' + code_six
        self.kiwoom.subscribe_stock_conclusion('2000',codes)
############################################


############종목수량, 매수/매도호가 #############
    def get_data(self):

        bid_price = self.kiwoom.bid_price
        ask_price = self.kiwoom.ask_price      
        self.kiwoom.get_amount()    
        # if self.check :
        #     self.kiwoom.get_amount()    
        # else:
        #     pass
        return self.kiwoom.amount,bid_price, ask_price

    
    def get_price(self):
        bid_price = self.kiwoom.bid_price
        ask_price = self.kiwoom.ask_price
        # earning = self.kiwoom.earning
        return bid_price, ask_price

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
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, '069500', leverage, price, '00', "")
        
    def sell_kodex200(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, '069500', leverage, price, '00', "")

    def buy_tiger200(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 1, '102110', leverage, price, '00', "")
        
    def sell_tiger200(self,price,leverage):
        self.kiwoom.SendOrder("send_order_req", "0101", self.account, 2, '102110', leverage, price, '00', "")
        
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
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.   25
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산


        ###초기 설정###
        leverage = 1
        init_count = 20

        kodex_200 = 'KODEX 200' 
        tiger_200 = 'TIGER 200'
        
        start_spread = 15
        finish_spread = -5

        if kodex_200 in amount.keys():
            amount_kodex_200 = amount[kodex_200]
        else:
            amount_kodex_200 = 0

        if tiger_200 in amount.keys():
            amount_tiger_200 = amount[tiger_200]
        else:
            amount_tiger_200 = 0


        ### get bid ask###
        if kodex_200 in bid_price.keys() and tiger_200 in bid_price.keys():            
            bid_kodex_200 = bid_price[kodex_200]  # 매수가격
            bid_tiger_200 = bid_price[tiger_200]
            ask_kodex_200 = ask_price[kodex_200]  # 매도가격
            ask_tiger_200 = ask_price[tiger_200]

            self.check = False

            if ask_kodex_200 - bid_tiger_200 >= start_spread and amount_tiger_200 <= (init_count*2-leverage) :  
                print('start position')   
                self.sell_kodex200(ask_kodex_200,leverage)
                self.buy_tiger200(bid_tiger_200,leverage)
                self.profit += ask_kodex_200 - bid_tiger_200
                self.check = True

            elif amount_tiger_200 > init_count and  ask_tiger_200 - bid_kodex_200 >= finish_spread :
                print('close position')
                self.sell_tiger200(ask_tiger_200,(amount_tiger_200-init_count))
                self.buy_kodex200(bid_kodex_200,(amount_tiger_200-init_count))
                self.profit += ask_tiger_200 - bid_kodex_200
                self.check = True
           
        print('profit :',self.profit)


                    
################################################### Algo_3##########################################################
    def three(self,amount,bid_price,ask_price):
        print('[algo_three]----------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. KODEX 인버스과 TIGER 인버스의 매수호가(매도가격) 스프레드가 지난 60개의 데이터 이동평균과 달라지는 경우,
        # 2. 매수호가,매도호가 스프레드를 고려하여 threshold에 반영.
        # 3. 숏 또는 롱 포지션 취한 후, 
        # 4. 반대 포지션으로 청산
        
        ###초기 설정###
        leverage = 1
        init_count = 10

        kodex_inv = 'KODEX 인버스' 
        tiger_inv = 'TIGER 인버스'
        spread = 400

        if kodex_inv in amount.keys():
            amount_kodex_inv = amount[kodex_inv]
        else: 
            amount_kodex_inv = 0

        if tiger_inv in amount.keys():
            amount_tiger_inv = amount[tiger_inv]
        else:
            amount_tiger_inv = 0


        ### get bid ask###
        if kodex_inv in bid_price.keys() and tiger_inv in bid_price.keys():            
            bid_kodex_inv = bid_price[kodex_inv]  # 매수가격
            bid_tiger_inv = bid_price[tiger_inv]
            ask_kodex_inv = ask_price[kodex_inv]  # 매도가격
            ask_tiger_inv = ask_price[tiger_inv]


            if ask_kodex_inv > bid_tiger_inv +spread+10 and amount_tiger_inv<=19:  
                print('short position')   
                self.sell_kodexinv(ask_kodex_inv,leverage)
                self.buy_tigerinv(bid_tiger_inv,leverage)

            elif ask_tiger_inv > bid_kodex_inv +spread+10 and amount_tiger_inv<=19 :
                print('long position')   
                self.sell_tigerinv(ask_tiger_inv,leverage)
                self.buy_kodexinv(bid_kodex_inv,leverage)                  


            if amount_tiger_inv > init_count and  bid_kodex_inv == ask_tiger_inv + spread :
                print('close position')
                self.sell_tigerinv(ask_tiger_inv,(amount_tiger_inv-init_count))
                self.buy_kodexinv(bid_kodex_inv,(amount_tiger_inv-init_count))

            elif amount_kodex_inv > init_count and  ask_kodex_inv + spread == bid_tiger_inv:
                print('close position')                    
                self.sell_kodexinv(ask_kodex_inv,(amount_kodex_inv-init_count))
                self.buy_tigerinv(bid_tiger_inv,(amount_kodex_inv-init_count))


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
        init_count = 5

        samsung = '삼성전자' 
        samsung_wu = '삼성전자우'

        spread = 10000

        if samsung in amount.keys():
            amount_samsung = amount[samsung]
        else:
            amount_samsung = 0

        if samsung_wu in amount.keys():
            amount_samsung_wu = amount[samsung_wu]
        else:
            amount_samsung_wu = 0


        ### get bid ask###
        if samsung in bid_price.keys() and samsung_wu in bid_price.keys():            
            bid_samsung = bid_price[samsung]  # 매수가격
            bid_samsung_wu = bid_price[samsung_wu]
            ask_samsung = ask_price[samsung]  # 매도가격
            ask_samsung_wu = ask_price[samsung_wu]


            if ask_samsung > bid_samsung_wu + spread + 200 and amount_samsung_wu<=9:  
                print('short position')   
                self.sell_samsung(ask_samsung,leverage)
                self.buy_samsung_wu(bid_samsung_wu,leverage)

            elif ask_samsung_wu > bid_samsung and amount_samsung <=9 :
                print('long position')   
                self.sell_samsung_wu(ask_samsung_wu,leverage)
                self.buy_samsung(bid_samsung,leverage)                  


            if amount_samsung > init_count and  ask_samsung == bid_samsung_wu + spread +100:
                print('close position')                    
                self.sell_samsung(ask_samsung,(amount_samsung-init_count))
                self.buy_samsung_wu(bid_samsung_wu,(amount_samsung-init_count))

            elif amount_samsung_wu > init_count and  bid_samsung +spread +100== ask_samsung_wu :
                print('close position')
                self.sell_samsung_wu(ask_samsung_wu,(amount_samsung_wu-init_count))
                self.buy_samsung(bid_samsung,(amount_samsung_wu-init_count))
        print('')


################################################### Algo_6########################################################## 

    def six(self,amount, bid_price, ask_price):
        print('[algo_six]--------------------------------------------------------------------')   
        
        ### 알고리즘 요약
        # 1. kodex_active와 tiger_active 매수호가(매수가격) 스프레드가 
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
        if 'KODEX 혁신기술테마액티브' in bid_price.keys() and 'TIGER AI코리아그로스액티브' in bid_price.keys():            
            bid_kodex_active = bid_price['KODEX 혁신기술테마액티브']  # 매수가격
            bid_tiger_active = bid_price['TIGER AI코리아그로스액티브']
            ask_kodex_active = ask_price['KODEX 혁신기술테마액티브']  # 매도가격
            ask_tiger_active = ask_price['TIGER AI코리아그로스액티브']


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
                self.sell_tiger(ask_tiger_active,(amount_tiger_active-init_count))
                self.buy_kodex(bid_kodex_active,(amount_tiger_active-init_count))
                    

        print('')
