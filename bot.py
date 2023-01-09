import Constants as keys
import logging
from telegram       import Update
from telegram.ext   import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from cleantext      import clean
import re

def my_split(s):
    return re.split('(\d+.\d+)', s)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# # function saves message to file
# async def save_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
#     signal_file = open(keys.FILE_PATH, 'w')
#     signal_file.write(clean(update.message.text, no_emoji=True))
#     signal_file.close()
    
#     convert_file()
    
#     print(update.message.text)
    
#function forward new message from channel to group
async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.forward_message(chat_id=keys.GROUP_ID, from_chat_id=keys.MY_SIGNALS_CHANNEL, message_id=update.effective_message.message_id)
    #print('***forwarded***')
    #print(update.effective_message.text)
    
    signal_file = open(keys.FILE_PATH, 'w')
    signal_file.write(clean(update.effective_message.text, no_emoji=True))
    signal_file.close()
    
    convert_file()
    
    #print(update.effective_message.text)

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

    # print(data_array)

    # save data_array to file
    file_name = open(keys.SAVE_PATH, 'w')
    file_name.write(str(data_array))
    file_name.close()
    
############################## MAIN ##############################
if __name__ == '__main__':
      
    #create application and use user api key
    application = ApplicationBuilder(keys.PERSONAL_API)
    
    #save_signal_handler = MessageHandler(filters.TEXT, save_signal)
    forward_message_handler = MessageHandler(filters.TEXT, forward_message)
     
    #application.add_handler(save_signal_handler)
    application.add_handler(forward_message_handler)
    
    application.run_polling()