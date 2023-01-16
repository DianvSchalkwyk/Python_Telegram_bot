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

MQL5 bot code:

#include <Trade\Trade.mqh>

CTrade trade;

string signal_string;
string seperator_sign = "|";
ushort seperator_code;
string signal_array[];
int    sub_string_count;
int    fileHandle;
bool   file_is_empty = true;
int    trades_made = 0;

string symbol_names;
string signal_type;
double signal_price;
double take_profit_1;
double take_profit_2;
double take_profit_3;
double take_profit_custom;
double stop_loss;
double position_size = 0.01;

double point;
double bid;
double open_price;
int    decimal_places;
double Ask;

void OnTick()
{
   Comment("Trades made: " + IntegerToString(trades_made));
   
   seperator_code = StringGetCharacter(seperator_sign, 0);
   
   fileHandle = FileOpen("signal.txt", FILE_READ|FILE_ANSI|FILE_COMMON, CP_ACP);
   
   if(fileHandle==INVALID_HANDLE) Alert("File Error");
   
   signal_string = FileReadString(fileHandle);
  
   //split string into array
   sub_string_count = StringSplit(signal_string, seperator_code, signal_array);
   
   if (ArraySize(signal_array) == 0)
   {
      file_is_empty = true;
      //Print("file_is_empty = true;");
   }
   else
   {
      file_is_empty = false;
      //Print("file_is_empty = false;");
   }
   
   FileClose(fileHandle);
   
   if(!file_is_empty)
   {
      for(int i = 0; i < SymbolsTotal(false); i++)
      {
         if(signal_array[0] == SymbolName(i, false))
         {
            symbol_names  = signal_array[0];
            signal_type   = signal_array[1];
            signal_price  = StringToDouble(signal_array[2]);
            take_profit_1 = StringToDouble(signal_array[3]);
            take_profit_2 = StringToDouble(signal_array[4]);
            take_profit_3 = StringToDouble(signal_array[5]);
            stop_loss     = StringToDouble(signal_array[6]);
            
            take_profit_custom = (take_profit_1+take_profit_2)/2;
            decimal_places     = (int)SymbolInfoInteger(symbol_names,SYMBOL_DIGITS);
            stop_loss          = NormalizeDouble(stop_loss,decimal_places);
            take_profit_custom = NormalizeDouble(take_profit_custom,decimal_places);
            point              = SymbolInfoDouble(symbol_names,SYMBOL_POINT);
            //bid                = SymbolInfoDouble(symbol_names,SYMBOL_BID);
            //open_price         = SymbolInfoDouble(symbol_names,SYMBOL_ASK);
            Ask                = NormalizeDouble(SymbolInfoDouble(_Symbol, SYMBOL_ASK), _Digits);
   
            Print("Symbol name: " , symbol_names);
            Print("Signal type: " , signal_type);
            Print("Signal price: ", signal_price);
            Print("Take profit: " , take_profit_custom);
            Print("Stop loss: "   , stop_loss);
            
            if(signal_type == "BUY")
            {
               trade.Buy(position_size, symbol_names, Ask, stop_loss, take_profit_custom);
               trades_made++;
            }
            else if(signal_type == "BUYLIMIT")
            {
               trade.BuyLimit(position_size, signal_price, symbol_names, stop_loss, take_profit_custom);
               trades_made++;
            }
            else if(signal_type == "SELL")
            {
               trade.Sell(position_size, symbol_names, Ask, stop_loss, take_profit_custom);
               trades_made++;
            }
            else if(signal_type == "SELLLIMIT")
            {
               trade.SellLimit(position_size, signal_price, symbol_names, stop_loss, take_profit_custom);
               trades_made++;
            }
            
            //clear file
            fileHandle = FileOpen("signal.txt", FILE_WRITE|FILE_ANSI|FILE_COMMON, CP_ACP);
            FileClose(fileHandle);
         }
      }
   }
}