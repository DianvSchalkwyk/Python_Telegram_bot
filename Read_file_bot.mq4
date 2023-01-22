//+------------------------------------------------------------------+
//|                                                    Read_file_bot |
//|                                https://github.com/DianvSchalkwyk |
//+------------------------------------------------------------------+
string signal_string;
string seperator_sign = "|";
ushort seperator_code;
string signal_array[];
int    sub_string_count;
int    fileHandle;
bool   file_is_empty = true;
bool   made_new_trade = false;
int    trades_made = 0;

string symbol_names;
string signal_type;
double signal_price;
double take_profit_1;
double take_profit_2;
double take_profit_3;
double take_profit_custom;
double stop_loss;
double stop_loss_half;
double position_size = 0.01;
int    slippage = 5;

double point;
double bid_price;
double ask_price;
int    decimal_places;
double ask_price2;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTick()
  {
   seperator_code = StringGetCharacter(seperator_sign, 0);

   fileHandle = FileOpen("signal.txt", FILE_READ);

   if(fileHandle==INVALID_HANDLE)
      Alert("File Error");

   signal_string = FileReadString(fileHandle);

   //split string into array
   sub_string_count = StringSplit(signal_string, seperator_code, signal_array);

   if(ArraySize(signal_array) == 0)
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
            
            point              = SymbolInfoDouble(symbol_names,SYMBOL_POINT);
            bid_price          = SymbolInfoDouble(symbol_names,SYMBOL_BID);
            ask_price          = SymbolInfoDouble(symbol_names,SYMBOL_ASK);

            stop_loss          = NormalizeDouble(stop_loss,decimal_places);
            take_profit_custom = NormalizeDouble(take_profit_custom,decimal_places);
            stop_loss_half     = NormalizeDouble(((ask_price + stop_loss)/2), decimal_places);

            Print("Symbol name: " , symbol_names);
            Print("Signal type: " , signal_type);
            Print("Signal price: ", signal_price);
            Print("Ask price: "   , ask_price);
            Print("Take profit: " , take_profit_custom);
            Print("Stop loss: "   , stop_loss);
            Print("Limit order: " , stop_loss_half);

            //You buy at the Ask and sell at the Bid
            if(signal_type == "BUY")
            {
               OrderSend(symbol_names,OP_BUY     , position_size, ask_price     , slippage, stop_loss, take_profit_custom);
               OrderSend(symbol_names,OP_BUYLIMIT, position_size, stop_loss_half, slippage, stop_loss, take_profit_custom);
            }
            else
            if(signal_type == "BUYLIMIT")
            {
               OrderSend(symbol_names,OP_BUYLIMIT, position_size, signal_price  , slippage, stop_loss, take_profit_custom);
               OrderSend(symbol_names,OP_BUYLIMIT, position_size, stop_loss_half, slippage, stop_loss, take_profit_custom);
            }
            else
            if(signal_type == "SELL")
            {
               OrderSend(symbol_names,OP_SELL     , position_size, bid_price     , slippage, stop_loss, take_profit_custom);
               OrderSend(symbol_names,OP_SELLLIMIT, position_size, stop_loss_half, slippage, stop_loss, take_profit_custom);
            }
            else
            if(signal_type == "SELLLIMIT")
            {
               OrderSend(symbol_names,OP_SELLLIMIT, position_size, signal_price  , slippage, stop_loss, take_profit_custom);
               OrderSend(symbol_names,OP_SELLLIMIT, position_size, stop_loss_half, slippage, stop_loss, take_profit_custom);
            }

            //clear file
            fileHandle = FileOpen("signal.txt", FILE_WRITE);
            FileClose(fileHandle);
           }
        }
     }
  }
//+------------------------------------------------------------------+
