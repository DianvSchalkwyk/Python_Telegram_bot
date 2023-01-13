import Constants as keys
import logging
import re

from telethon   import TelegramClient, events
from cleantext  import clean

api_id      = keys.PERSONAL_API
api_hash    = keys.PERSONAL_HASH
client      = TelegramClient('anon', api_id, api_hash)

client.start()

def my_split(s):
    return re.split('(\d+.\d+)', s)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def convert_file():
    
    file_name = open(keys.FILE_PATH, 'r')

    # split file_name string into array
    data_array = file_name.read().splitlines()
    print(data_array[0])

    #if first element of data_array in upper case is NOT equal to an item in the CURRENCIES_LIST, then exit the function
    if data_array[0].upper() not in keys.TRADE_LIST:
        print('not in list')
        return

    # if last element of data_array does not start with sl, then delete it
    if not data_array[-1].startswith('sl'):
        data_array.pop()

    data_array[1] = my_split(data_array[1])

    # if data_array[1] has 3 elements, then delete the last one
    if len(data_array[1]) == 3:
        data_array[1].pop()
        
    #remove element 2 from data_array
    signal_type = data_array.pop(1)
    
    signal_part_1 = signal_type[0]
    signal_part_2 = signal_type[1]

    #insert signal_part_1 and signal_part_2 into data_array after element 0
    data_array.insert(1, signal_part_1)
    data_array.insert(2, signal_part_2)

    #replace tp1:, tp2:, tp3:, sl-, " " and : with ""
    for i in range(len(data_array)):
        data_array[i] = data_array[i].replace('tp1:', '')
        data_array[i] = data_array[i].replace('tp2:', '')
        data_array[i] = data_array[i].replace('tp3:', '')
        data_array[i] = data_array[i].replace('sl-', '')
        data_array[i] = data_array[i].replace(' ', '')
        data_array[i] = data_array[i].replace(':', '')

    #put data_array into a string, each element separated by a |
    data_array = '|'.join(data_array)

    # save data_array to file
    file_name = open(keys.SAVE_PATH, 'w')
    file_name.write(str(data_array))
    file_name.close()

@client.on(events.NewMessage(chats=-1001481257205))
async def main(event):

    signal_file = open(keys.FILE_PATH, 'w')
    signal_file.write(clean(event.message.text, no_emoji=True))
    signal_file.close()
    
    convert_file()

    await client.forward_messages(-890927419, event.message)

with client:
    client.run_until_disconnected()