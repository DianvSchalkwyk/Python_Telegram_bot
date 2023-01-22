import Constants as keys
import re

'''function to split te signal type and the buy price into 2 different elements'''
def my_split(string_to_split):
    return re.split('(\d+.\d+)', string_to_split)

'''function to check if the signal is valid, if it is, it will be formatted and saved to a file'''
def convert_file():
    
    file_name = open(keys.FILE_PATH, 'r')

    # split file_name string into array and make all upper case
    data_array = file_name.read().upper().splitlines()
    print(data_array[0])

    #if first element of data_array in upper case is NOT equal to an item in the CURRENCIES_LIST, then clear the file content and exit the function
    if data_array[0].upper() not in keys.TRADE_LIST:
        file_name = open(keys.FILE_PATH, 'w')
        file_name.write('')
        file_name.close()
        print('Signal received not valid.')
        return

    # remove last element of array, it is usually just a message to move the stoploss
    data_array.pop()

    # split data_array[1] into 2 elements
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
        for j in range(len(keys.REMOVE_LIST)):
            data_array[i] = data_array[i].replace(keys.REMOVE_LIST[j], '')

    #put data_array into a string, each element separated by a |
    data_array = '|'.join(data_array)

    global new_signal
    new_signal = str(data_array)

    # save data_array to file
    file_name = open(keys.FILE_PATH, 'w')
    file_name.write(str(data_array))
    file_name.close()