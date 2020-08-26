from telethon import TelegramClient, events, sync
from threading import Thread
from iqoptionapi.stable_api import IQ_Option



# Remember to use your own values from my.telegram.org!
api_id = 1677969
api_hash = '7d1e424765873c884a799f4623957fbe'
client = TelegramClient('+213553301252', api_id, api_hash)


class trading:

    def __init__(self, ACTIVES, ACTION, expirations_mode, I_want_money):
        self.Money = 1
        self.ACTIVES = ACTIVES
        self.ACTION = ACTION
        self.expirations_mode = expirations_mode
        self.I_want_money = I_want_money


    def connect():
    	I_want_money=IQ_Option("mahcara87@gmail.com","gikoulekikou")
    	check, reason = I_want_money.connect()
    	if check:
    		print('Bot enabled')
    		I_want_money.change_balance("PRACTICE")
    		return I_want_money

    def go(self):
    	print(self.ACTIVES)
    	goal= self.ACTIVES
    	if self.expirations_mode != 0:
        	check, id = self.I_want_money.buy(self.Money,self.ACTIVES,self.ACTION,self.expirations_mode)
        	profit = self.I_want_money.check_win_v3(id)
        	print((str(id))+ ' Profit = ' + str(profit))
        	if profit <= 0:
        		Money = self.Money * 2
        		check, id = self.I_want_money.buy(Money,self.ACTIVES,self.ACTION,self.expirations_mode)
        		print(str(id)+ ' Profit = ' + str(profit))


I_want_money = trading.connect()


@client.on(events.NewMessage(chats='boption100'))
async def my_event_handler(event):
	message = event.raw_text
	message = message.split()
	if message[1].upper() == 'CALL':
		ACTION = 'call'
	else:
		ACTION = 'put'

	ACTIVES = message[2][:6]
	Minutes = message[2]
	time = ''
	for s in Minutes: 
		if s.isdigit(): 
			time = time+str(s)

	Minutes = int(time)

	tradingVar = trading(ACTIVES,ACTION,Minutes, I_want_money)
	Thread(target=tradingVar.go, args=()).start()

client.start()
client.run_until_disconnected()


