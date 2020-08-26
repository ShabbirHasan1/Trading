import asyncio
from telethon import TelegramClient
from telethon.tl import functions, types

api_id = 1677969
api_hash = '7d1e424765873c884a799f4623957fbe'

client = TelegramClient('anon', api_id, api_hash)
client.start()

async def main():
    channel = await client.get_entity(-1001296890742)
    messages = await client.get_messages(channel, limit= 10) #pass your own args

    #then if you want to get all the messages text
    for x in messages:
        print(x.text) #return message.text


loop = asyncio.get_event_loop()
loop.run_until_complete(main())