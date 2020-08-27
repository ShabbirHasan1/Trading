from telethon import TelegramClient, events, sync
from iqoptionapi.stable_api import IQ_Option
import time
import calendar
import requests
import json, logging
import os
from threading import Thread
import sys

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')


api_id = 1677969
api_hash = '7d1e424765873c884a799f4623957fbe'
client = TelegramClient('ali_programmer29', api_id, api_hash)

class trading:
    def __init__(self, token,email, password, amount):
        self.token = token
        self.password = password
        self.email = email
        self.amount = int(amount)
        
    def connect(self):
        if self.subscription == 'on':
            self.connected =IQ_Option(self.email,self.password)
            check,reason=self.connected.connect()
            self.connected.change_balance("PRACTICE")
            
            if check:
                print("Bot is enabled now")   
                print("Your balance is: " + str(self.connected.get_balance()))
                print('-------------------------------------')
                print("Waiting for telegrames messages...")      
                print('-------------------------------------')               
            else:
                if reason=="[Errno -2] Name or service not known":
                    print("No Network")
                elif reason=="error_password":
                    print("Error Password")
        else:
            sys.exit("Their is no subscription with this email")
    
    def reconnect(self):
        while True:
            time.sleep(300)
            check,reason=self.connected.connect()

    def makeTrade(self):
        print(self.subscription)
        print(self.active)
        print(self.action)
        print(self.duration)
        if self.subscription == 'on':            
            check,id = self.connected.buy(1,self.active,self.action,self.duration)
            profit = self.connected.check_win_v3(id)
            if profit == 0:
                print(str(self.active) + '  '+ str(self.action) + '  ' + str(self.duration) + ' ' + str(profit) + ' ')
            elif profit > 0:
                print(str(self.active) + '  '+ str(self.action) + '  ' + str(self.duration) + '  ' + str(profit) + ' ')
            else:
                print(str(self.active) + '  '+ str(self.action) + '  ' + str(self.duration) + '  ' + str(profit) + ' ')
            print('-------------------------------------')

    def check_subscription(self):
        url = "https://trading.cocktillo.com/trading-api/public/api/check?email="+self.email+"&token="+self.token
        try:
            r = requests.get(url)
            data = r.json()
            self.subscription = data['status']
            if self.subscription != 'on':
                sys.exit("Their is no subscription with this email")
        except:
            self.subscription = 'exception'
            sys.exit("Connection problem!")

    def recheck_subscription(self):
        url = "https://trading.cocktillo.com/trading-api/public/api/check?email="+self.email+"&token="+self.token
        while True:
            time.sleep(300)
            try:
                r = requests.get(url)
                data = r.json()
                self.subscription = data['status']
                if self.subscription != 'on':
                    sys.exit("Their is no subscription with this email")
            except:
                self.subscription = 'exception'
                sys.exit("Connection problem!")
  

token = input("Token:") or "123"
email = input("Email:") or "ali.benali.pro@gmail.com"
password = input("Password:") or "BDC252B29EAli"
money = input("Amount:") or "1"
myTrading = trading(token,email, password, money)
myTrading.check_subscription()
myTrading.connect()
Thread(target=myTrading.reconnect, args=()).start()
Thread(target=myTrading.recheck_subscription, args=()).start()
 

############################################

@client.on(events.NewMessage(chats=-1001463916752))
async def my_event_handler(event):
    message = event.raw_text.upper()
    print(message)
    message = message.split()
    if message[0] == 'GO':
        Thread(target=myTrading.makeTrade, args=()).start()
    else:
        myTrading.action= ''
        myTrading.active= ''
        myTrading.duration= ''
        
    if message[2] == 'CALL':
        myTrading.action = 'call'
    else:
        myTrading.action = 'put'
    myTrading.active = message[0]+message[1]
    duration = int(message[3])
    if duration == 1:
        myTrading.duration = 1
    elif duration == 5:
        myTrading.duration = 65
    elif duration == 15:
        myTrading.duration = 75
    elif duration == 25:
        myTrading.duration = 80
    
client.start()
client.run_until_disconnected()


