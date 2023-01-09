'''build telegram bot that sends messages to MT4'''

import Constants as keys
import Responses as responses

import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

print("Bot started...")

def start_command(update, context):
    update.message.reply_text('Type something random to get started!')
    
def help_command(update, context):
    update.message.reply_text('If you need help, please search Google')
    
def handle_message(update, context):
    text = str(update.message.text).lower()
    response = responses.sample_responses(text)
    
    update.message.reply_text(response)
    
def error(update, context):
    print(f"Update {update} caused error {context.error}")
    
def main():
    updater = Updater(keys.API_KEY , use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler(filters.TEXT, handle_message))
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()
    
main()

