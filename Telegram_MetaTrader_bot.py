import constants as keys
import logging
import re

from functions import *

from telethon   import TelegramClient, events
from cleantext  import clean

client = TelegramClient('anon', keys.PERSONAL_API, keys.PERSONAL_HASH)

client.start()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

@client.on(events.NewMessage(chats=keys.FOREX_CHANNEL_ID))
@client.on(events.NewMessage(chats=keys.MY_CHANNEL)) 

async def main(event):

    signal_file = open(keys.FILE_PATH, 'w')
    signal_file.write(clean(event.message.text, no_emoji=True))
    signal_file.close()
    
    convert_file()

    #send new_signal to group if new_signal is not empty, else send "no signal"
    if keys.NEW_SIGNAL != "":
        await client.send_message(keys.GROUP_ID, keys.NEW_SIGNAL)
    else:
        await client.send_message(keys.GROUP_ID, "Message received, but not a signal.")

with client:
    client.run_until_disconnected()