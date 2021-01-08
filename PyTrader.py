import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Algos import *
import time
from datetime import datetime,timedelta


now = datetime.now()
form_class = uic.loadUiType("_pytrader.ui")[0]


app = QApplication(sys.argv)
algo = Algos()
print('-------------------------------거래시작------------------------------------')
while now.strftime('%H%M%S') != 152101:
    algo.one()
    time.sleep(3)
app.exec_() 
