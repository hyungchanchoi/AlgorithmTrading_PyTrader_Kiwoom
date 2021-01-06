import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        
        self.price = {}
        self.rate = {}
        self.amount = {}
        self.bid_price = {} #매수호가
        self.ask_price = {} #매도호가
        
#         self.dynamicCall("SetRealReg(QString,QString,QString,QString)", '0101','','215','0')  #실시간구분

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
#         self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.OnReceiveRealData.connect(self._receive_real_data)
        
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)
            

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                     [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])
        
    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        ret_ = ret.rstrip()
        return ret_
    
    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print('[',self.get_chejan_data(908),']',self.get_chejan_data(302),':',self.get_chejan_data(905), 
                     self.get_chejan_data(900),'주',self.get_chejan_data(10),'원')
        self.amount[self.get_chejan_data(302)] = self.get_chejan_data(930)

    def get_real_data(self,code): 
#         print(1,code)
        self.dynamicCall("SetRealReg(QString,QString,QString,QString)", '1000',code,'568','1')
        self.real_event_loop = QEventLoop()
        self.real_event_loop.exec_()
            
    def _receive_real_data(self, code, realtype, realdata):   
#         print(2,code)
        temp_ask_price = self.dynamicCall("GetCommRealData(QString,int)",code,27)  #매도호가
        temp_bid_price = self.dynamicCall("GetCommRealData(QString,int)",code,28)  #매수호가
        temp_price = self.dynamicCall("GetCommRealData(QString,int)",code,10)
        temp_rate = self.dynamicCall("GetCommRealData(QString,int)",code,12)                  
        self.price[code] = int(temp_price)
        self.rate[code] = float(temp_rate)
        self.bid_price[code] = int(temp_bid_price)
        self.ask_price[code] = int(temp_ask_price)
        self.real_event_loop.exit()

                        
    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret 

    def get_server_gubun(self):
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret