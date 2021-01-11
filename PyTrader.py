import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Algos import *
from Kiwoom import *
import time
from datetime import datetime,timedelta
# form_class = uic.loadUiType("_pytrader.ui")[0]


############################## 트레이딩 ##################################
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    algo = Algos()

    print('-------------------------------거래시작------------------------------------')
    while now.strftime('%H%M%S') != 152101:
        
        ####현재시간####
        now = datetime.now()
        print(now.strftime('%H%M%S'))

        ####종목수량,매도/매수호가####
        amount,bid_price,ask_price = algo.get_data()

        ###알고리즘###
        algo.one(amount,bid_price,ask_price)
        # algo.two(amount,bid_price,ask_price)

        time.sleep(1)

    app.exec_() 





