import Constants as keys
import re

def my_split(s):
    return re.split('(\d+.\d+)', s)

file_name = open(keys.FILE_PATH, 'r')

# split file_name string into array
data_array = file_name.read().splitlines()

#if first element of data_array is NOT equal to an item in the CURRENCIES_LIST, the stop the program
if data_array[0] not in keys.CURRENCIES_LIST:
    print("Error: currency not in CURRENCIES_LIST")
    exit()

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

#replace tp1: and tp2: and tp3: and sl- with ""
for i in range(len(data_array)):
    data_array[i] = data_array[i].replace('tp1:', '')
    data_array[i] = data_array[i].replace('tp2:', '')
    data_array[i] = data_array[i].replace('tp3:', '')
    data_array[i] = data_array[i].replace('sl-', '')
    data_array[i] = data_array[i].replace(' ', '')
    data_array[i] = data_array[i].replace(':', '')
    
#put data_array into a string, each element separated by a |
data_array = '|'.join(data_array)

print(data_array)

# save data_array to file
file_name = open(keys.SAVE_PATH, 'w')
file_name.write(str(data_array))
file_name.close()