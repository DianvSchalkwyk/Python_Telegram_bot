import constants as keys
import re

'''function to split te signal type and the buy price into 2 different elements'''
def my_split(string_to_split):
    return re.split('(\d+.\d+)', string_to_split)

'''function to check if the signal is valid, if it is, it will be formatted and saved to a file'''
def convert_string(signal_string_to_convert):
    
    #create signal_pair, data_array and NEW_SIGNAL as global variables
    data_array = []

    signal_string = signal_string_to_convert

    #remove all : and - from signal_string
    signal_string = signal_string.replace(":", " ")
    signal_string = signal_string.replace("-", " ")
    
    #split signal_string into data_received where there is a space or a new line
    data_received = re.split(r'\s|\n', signal_string)

    #remove all empty elements that contain "" or " " from data_receive
    data_received = list(filter(None, data_received))

    #loop through array and make all elements uppercase
    for i in range(len(data_received)):
        data_received[i] = data_received[i].upper()

    #loop through array and get element that contains the signal pair, if found, add to data_array and break loop
    for i in range(len(data_received)):
        if data_received[i] in keys.TRADE_LIST:
            data_array.append(data_received[i])
            break

    #if data_array is empty, exit function
    if not data_array:
        print("Not a valid signal")
        return

    #loop through data_reveived, use regext to check for "BUY" or "SELL" and append to data_array
    for i in range(len(data_received)):
        if re.search(r'BUY|SELL', data_received[i]):
            data_array.append(data_received[i])
        
            #loop through the rest of data_reveived and use regext to check for a number and append to data_array
            for j in range(i+1, len(data_received)):
                if re.search(r'\d+.\d+', data_received[j]):
                    data_array.append(data_received[j])
                    break
            
            break

    #loop through data_reveived, use regext to check for TP/TP1/TAKE PROFIT/TAKEPROFIT
    for i in range(len(data_received)):
        if re.search(r'TP|TP1|TP.|TP1.|TAKE PROFIT|TAKEPROFIT', data_received[i]):
        
            #append the next element as the take profit price to use for the trade
            data_array.append(data_received[i+1])

            break

    #loop through data_reveived, use regext to check for SL/SL1/STOP LOSS/STOPLOSS
    for i in range(len(data_received)):
        if re.search(r'SL|SL1|SL.|STOP LOSS|STOPLOSS', data_received[i]):
        
            #append the next element as the stop loss price to use for the trade
            data_array.append(data_received[i+1])

            break

    # loop through data_reveived, use regext to check for 10PIP/10PIPS/10 PIP/10 PIPS
    for i in range(len(data_received)):
        if re.search(r'10PIP|10PIPS|10 PIP|10 PIPS', data_received[i]):
            data_array.append("PIPS10")
            break

    #loop through data_array, if it does not contain PIPS10, append NORMAL
    if "PIPS10" not in data_array:
        data_array.append("NORMAL")
        
    '''if data_array 0 is not in keys.TRADE_LIST,
    or data_array 1 is not BUY or SELL,
    or data_array 2 is not a number,
    or data_array 3 is not a number,
    or data_array 4 is not a number
    or data_array 5 is not PIPS10 or NORMAL,
    exit function
    '''
    if data_array[0] not in keys.TRADE_LIST or data_array[1] not in ["BUY", "SELL"] or not re.search(r'\d+.\d+', data_array[2]) or not re.search(r'\d+.\d+', data_array[3]) or not re.search(r'\d+.\d+', data_array[4] or data_array[5] not in ["PIPS10", "NORMAL"]):
        print("Not a valid signal")
        return

    #save data_array to new string, split elements with |
    data_array = "|".join(data_array)

    #save data_array to keys.NEW_SIGNAL so it can be sent to group
    keys.NEW_SIGNAL = data_array

    print(data_array)

    # save data_array to file
    file_name = open(keys.FILE_PATH, 'w')
    file_name.write(str(data_array))
    file_name.close()