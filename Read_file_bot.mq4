//+------------------------------------------------------------------+
//|                                                    Read_file_bot |
//|                                https://github.com/DianvSchalkwyk |
//+------------------------------------------------------------------+
#property version   "1.00"
#property strict

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
double position_size_half = (position_size/2);
int    slippage = 5;
string stop_loss_type;

double point;
double bid_price;
double ask_price;
int    decimal_places;
double ask_price2;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   seperator_code = StringGetCharacter(seperator_sign, 0);

   fileHandle = FileOpen("signal.txt", FILE_READ);
   
   if(fileHandle==INVALID_HANDLE)
   {
      Alert("File Error");
   }
   
   signal_string = FileReadString(fileHandle);

   //split string into array
   sub_string_count = StringSplit(signal_string, seperator_code, signal_array);

   //if(ArraySize(signal_array) == 0)
   //{
   //   file_is_empty = true;
   //   Print("file_is_empty = true;");
   //}
   //else
   //{
   //   file_is_empty = false;
   //   Print("file_is_empty = false;");
   //}

   FileClose(fileHandle);

   if(!file_is_empty)
   {  
      for(int i = 0; i < SymbolsTotal(false); i++)
      {
         if(signal_array[0] == SymbolName(i, false))
         {
            symbol_names   = signal_array[0];
            signal_type    = signal_array[1];
            signal_price   = StringToDouble(signal_array[2]);
            take_profit_1  = StringToDouble(signal_array[3]);
            stop_loss      = StringToDouble(signal_array[4]);
            stop_loss_type = signal_array[5];
            
            decimal_places     = (int)SymbolInfoInteger(symbol_names,SYMBOL_DIGITS);
            
            point              = SymbolInfoDouble(symbol_names,SYMBOL_POINT);
            bid_price          = SymbolInfoDouble(symbol_names,SYMBOL_BID);
            ask_price          = SymbolInfoDouble(symbol_names,SYMBOL_ASK);
   
            stop_loss          = NormalizeDouble(stop_loss,decimal_places);
            take_profit_custom = NormalizeDouble(take_profit_custom,decimal_places);
   
            Print("Symbol name: "   , symbol_names);
            Print("Signal type: "   , signal_type);
            Print("Signal price: "  , signal_price);
            Print("Ask price: "     , ask_price);
            Print("Take profit: "   , take_profit_1);
            Print("Stop loss: "     , stop_loss);
            Print("Stop loss type: ", stop_loss_type);
   
            //You buy at the Ask and sell at the Bid
            if(signal_type == "BUY")
            {
               //open new buy order, put stop_loss_type in comment
               OrderSend(symbol_names, OP_BUY, position_size, ask_price, slippage, stop_loss, take_profit_1, stop_loss_type);
            }
            else if(signal_type == "SELL")
            {
               //open new sell order, put stop_loss_type in comment
               OrderSend(symbol_names, OP_SELL, position_size, bid_price, slippage, stop_loss, take_profit_1, stop_loss_type);
            }
   
            //clear file
            fileHandle = FileOpen("signal.txt", FILE_WRITE);
            FileClose(fileHandle);
         }
      }
   }

   // if there are any open orders, loop through them
   if(OrdersTotal() > 0)
   {
      for(int j = 0; j < OrdersTotal(); j++)
      {
         if(OrderSelect(j, SELECT_BY_POS, MODE_TRADES))
         {   
            //if order profit is >= 100 points, check if stop_loss_type is PIPS10 or NORMAL
            if((OrderProfit()/OrderLots()/MarketInfo(OrderSymbol(), MODE_TICKVALUE)) >= 100.0)
            {
               //if stop_loss_type is PIPS10, move stop loss to breakeven
               if(OrderComment() == "PIPS10")
               {
                  //check if order has not already been moved to breakeven
                  if(OrderStopLoss() != OrderOpenPrice())
                  {
                     //move stop loss to breakeven
                     OrderModify(OrderTicket(),OrderOpenPrice(),OrderOpenPrice(),OrderTakeProfit(),0,0);
                  }
               }
            }
         }
      }
   }
         
   
  }
//+------------------------------------------------------------------+
