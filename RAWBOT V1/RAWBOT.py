from iqoption.iqoptionapi.stable_api import IQ_Option
from time import gmtime, sleep
from calendar import timegm
from requests import get
import json, logging
from threading import Thread
from sys import exit
from getpass import getpass
from datetime import datetime

logging.disable(level=(logging.DEBUG))

class trading:

    def __init__(self, token,email, password, amount, stoploss):
        self.token = token
        self.password = password
        self.email = email
        self.amount = int(amount)
        self.stoploss = int(stoploss) * -1
        self.total = 0
    def connect(self):
        if self.subscription['status'] == 'on':
            self.connected =IQ_Option(self.email,self.password)
            check,reason=self.connected.connect()
            self.connected.change_balance("PRACTICE")
            if check:
                print("Bot is enabled now")                    
                print("Waiting for trades to copy...")                    
            else:
                check,reason=self.connected.connect()
                if check:
                    if reason=="[Errno -2] Name or service not known":
                        print("No Network")
                    elif reason==error_password:
                        print("Error Password")
        else:
            exit("Their is no subscription with this email")
    
    def reconnect(self):
        while True:
            sleep(60)
            check,reason=self.connected.connect()

    def get_practice_trades(self):
        passed = []
        while True:
            if self.connected.get_option_open_by_other_pc()!={}:
                ids=list(self.connected.get_option_open_by_other_pc().keys())
                for id in ids:
                    trade = self.connected.get_option_open_by_other_pc()[id]
                    if id not in passed:
                        self.ACTION = trade['msg']["dir"]
                        self.ACTIVES = trade['msg']["active"]
                        self.EXPIRATION = trade['msg']["exp_time"]
                        self.OPTION = trade['msg']["type_name"]
                        self.NOW = trade['msg']["now"]
                        if (trade['msg']['amount']/1000000) != self.amount:
                            f = open("debug.txt", "a")
                            f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), trade['msg']))
                            f.close()
                            Thread(target=self.makeTrade).start()
                            passed.append(id)
                    self.connected.del_option_open_by_other_pc(id)


    def makeTrade(self):
        if self.subscription['status'] == 'on':
            if self.total > self.stoploss:
                ACTION = self.ACTION
                ACTIVES = self.ACTIVES
                EXPIRATION = self.EXPIRATION
                OPTION = self.OPTION
                NOW = self.NOW
                self.connected.change_balance("REAL")
                check,id=self.connected.buy_by_raw_expirations(self.amount, ACTIVES, ACTION, OPTION,EXPIRATION)
                self.connected.change_balance("PRACTICE")
                profit = self.connected.check_win_v3(id)
                print(str(ACTION)+' '+ str(ACTIVES)+' '+ str(EXPIRATION)+' '+ str(OPTION)+' '+ str(NOW))
                if profit == 0:
                    print(str(id)+' (Equal) Profit:     '+str(profit))
                elif profit > 0:
                    print(str(id)+'(Win) Profit:        '+str(profit))
                else:
                    print(str(id)+'(Loose) Profit:      '+str(profit))
                self.total += int(profit)
        else:
            print(self.subscription['message'])
            
                    
    def check_subscription(self): 
        url = "https://trading.cocktillo.com/trading-api/public/api/check?email="+self.email+"&token="+self.token
        try:
            r = get(url)
            data = r.json()
            self.subscription = data

        except:
            self.subscription = 'exception'


    def recheck_subscription(self):
        url = "https://trading.cocktillo.com/trading-api/public/api/check?email="+self.email+"&token="+self.token
        while True:
            sleep(10)
            try:
                r = get(url)
                data = r.json()
                self.subscription = data
            except:
                self.subscription = data


token = input("Token:") or ""
email = input("Email:") or ""
password = getpass("Password:") or ""
money = input("Amount:") or "1"
stoploss = input("stop loss:") or "10"
myTrading = trading(token,email, password, money, stoploss)
myTrading.check_subscription()
myTrading.connect()
Thread(target=myTrading.get_practice_trades).start()
Thread(target=myTrading.reconnect).start()
Thread(target=myTrading.recheck_subscription).start()
