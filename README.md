# Python_Telegram_bot
 Telegram bot build in Python

1- This bot is used for a very specific telegram group which sends forex signals in it's own format. 
2- If you want to use this bot, you'll have to work on the convert_file function in the functions file. 
3- The bot will read the message the group sends, convert it and save it in the correct format. 
4- The MQL EA will then read the file and create a new order based on what the signal was.

You'll have to enter all the perameters in the 'Your_constants' file, then set the 'Telegram_MetaTrader_bot' to use that file, and then run the bot. At the moment it is set to use my own 'constants' file which is part of the .gitignore file.

The bot will then run and wait for a signal to be sent in the forex channel. Once it is sent, it will convert it and save it in the correct format. The MQL EA will then read the file and create a new order based on what the signal was. 

The bot will then send a message to the group saying that it has received the signal. If it was not a valid trading signal, it will send a message saying that it was not a valid signal. If it was a valid signal, it will send that message to your group.

Please note, this bot is not perfect and will not work for all signals. It is only designed to work for the signals that I use. If you want to use it, you'll have to work on the convert_file function in the functions file.

If you have any questions, please feel free to contact me.

P.S: the @client.on(events.NewMessage(chats=keys.MY_CHANNEL)) is used to listen for messages in my own channel I use to test the bot. You can remove it if you want.