
# coding: utf-8

# In[3]:


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from _Kiwoom import *
from _algos import *
import time
from datetime import datetime,timedelta

now = datetime.now()
form_class = uic.loadUiType("_pytrader.ui")[0]


# # 트레이딩

# In[ ]:

print(1)
app = QApplication(sys.argv)
algo = Algos()
app.exec_() 
print('-------------------------------거래시작------------------------------------')
while now.strftime('%H%M%S') != 152101:
    algo.zero()
    time.sleep(1)

