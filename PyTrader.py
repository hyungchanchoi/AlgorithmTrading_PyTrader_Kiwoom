import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Algos import *
from Kiwoom import *
import time
from datetime import datetime,timedelta
# form_class = uic.loadUiType("_pytrader.ui")[0]


############################## trading ##################################
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    algo = Algos()

    start = input('Did you check the initial condition of Algorithm? (yes or no) :')
    print('------------------------------- start trading ------------------------------------')    
    while start == 'yes' :
        
        #### current time ####
        now = datetime.now()
        if int(now.strftime('%H%M%S')) > 155000:
            break
        else:
            print('---',now.strftime('%H%M%S'),'---')

        #### num,bid,ask of stock ####
        amount,bid_price,ask_price = algo.get_data()

        ### Algorithm ###
        # algo.one(amount,bid_price,ask_price)
        # algo.two(amount,bid_price,ask_price)
        algo.three(amount,bid_price,ask_price)

        time.sleep(1.2)

    app.exec_() 





