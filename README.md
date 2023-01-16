# Python_Telegram_bot
 Telegram bot build in Python

You'll need to create your own 'Constants.py' file with your own API key and chat ID. You can get your own API key from the Telegram BotFather. You can get your own chat ID by sending a message to your bot and then going to https://api.telegram.org/bot<YourBOTToken>/getUpdates. You'll see a JSON response with your chat ID.    

You can also use the 'get_chat_id.py' file to get your chat ID. Just run the file and send a message to your bot. The chat ID will be printed to the console.

Constants.py file contents:

BOT_API = ''
BOT_ID = ''
FOREX_CHANNEL_ID = 
MY_SIGNALS_CHANNEL = 
GROUP_ID = 
PERSONAL_API = 
PERSONAL_HASH = 
FILE_PATH = ''
TRADE_LIST = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD',
            'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY',
            'XAUUSD', 'XAGUSD', 'XPTUSD', 'XPDUSD', 'XBRUSD', 'XNGUSD', 'XCUUSD', 'XPDUSD']
REMOVE_LIST = []