import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Algos import *
from Kiwoom import *
import win32com.client
import time
from datetime import datetime,timedelta
# form_class = uic.loadUiType("_pytrader.ui")[0]


############################## trading ##################################
if __name__ == "__main__":

    # 대신증권 연결 확인
    # instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    # print(instCpCybos.IsConnect)

    app = QApplication(sys.argv)
    algo = Algos()

    start = input('Did you check the initial condition of Algorithm? (yes or no) :')
    print('------------------------------- start trading ------------------------------------')    
    while True :
        
        ### current time ####
        now = datetime.now()
        if int(now.strftime('%H%M%S')) > 155000:
            break
        else:
            print('---',now.strftime('%H%M%S'),'---')


        #### num,bid,ask of stock ####
        # algo.kiwoom.get_profit()
        amount,bid_price, ask_price = algo.get_data()

        print('bid_price',bid_price)
        print('ask_price',ask_price)


        ### Algorithm ###
        # algo.zero(amount,bid_price,ask_price)
        # algo.one()
        # algo.two(amount,bid_price,ask_price)
        # algo.three(amount,bid_price,ask_price)    
        # algo.four(amount,bid_price,ask_price)
        algo.five(amount, bid_price, ask_price)
        algo.six(amount,bid_price,ask_price)

        time.sleep(2)


    app.exec_() 





