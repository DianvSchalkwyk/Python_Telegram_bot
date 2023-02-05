import logging

from functions import *
from telethon  import TelegramClient, events
from cleantext import clean

client = TelegramClient('anon', keys.PERSONAL_API, keys.PERSONAL_HASH)

client.start()

#set the logging level to info    
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#listen to the forex channel for new messages
@client.on(events.NewMessage(chats=keys.FOREX_CHANNEL_ID))
@client.on(events.NewMessage(chats=keys.MY_CHANNEL))

async def main(event):

    #copy event.message.text to signal_string and clean signal_string from emojis and line breaks
    signal_string = clean(event.message.text, no_emoji=True, no_line_breaks=True, lower=False)
    
    #send signal_string to convert_string() to check if it is a valid signal
    convert_string(signal_string)

    #if the message was a valid signal, send it to the group, otherwise send a message that the message was not a valid signal
    if keys.NEW_SIGNAL != "":
        await client.send_message(keys.GROUP_ID, keys.NEW_SIGNAL)
        
        #set key.NEW_SIGNAL to "" so that the next signal can be checked
        keys.NEW_SIGNAL = ""

    else:
        await client.send_message(keys.GROUP_ID, "Message received, but not a signal.")

with client:
    client.run_until_disconnected()