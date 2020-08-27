from iqoptionapi.stable_api import IQ_Option
import logging
import time
I_want_money=IQ_Option("ali.benali.pro@gmail.com","BDC252B29EAli")
I_want_money.connect()
I_want_money.change_balance("PRACTICE")

Money=1
ACTIVES="EURUSD"
ACTION="call"#or "put"
expirations_mode= int(input('Enter number:'))

check,id=I_want_money.buy(Money,ACTIVES,ACTION,expirations_mode)
