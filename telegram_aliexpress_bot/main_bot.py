#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.

# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from ConfigParser import SafeConfigParser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Show me an otter!", callback_data='1'),
                 InlineKeyboardButton("Next item", callback_data='2')],

                [InlineKeyboardButton("Create Link", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def new(bot, update):
    reply_keyboard = [['Show me an otter!', 'Next item'], 
                   ['Make Link', 'Close']]

    response = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text("what do you want", reply_markup=response)

    # oh wow i suck at this
    if response == 'Show me an otter!':
        bot.send_photo(chat_id=query.message.chat_id, photo='https://seaotters.com/wp-content/uploads/2012/03/628x353-otter-cu-yawn.jpg', message_id=query.message.message_id)
       
    elif response == 'Close':
        close_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
def button(bot, update):
    query = update.callback_query
    if query.data == '1':
        bot.send_photo(chat_id=query.message.chat_id, photo='https://seaotters.com/wp-content/uploads/2012/03/628x353-otter-cu-yawn.jpg', message_id=query.message.message_id)

    else:
        
        bot.edit_message_text(text="Selected option: {}".format(query.data),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Import api key
    parser = SafeConfigParser()
    parser.read('config.ini')
    botappkey = parser.get('Telegram', 'token')
    
    # Create the Updater and pass it your bot's token.
    updater = Updater(botappkey)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('new', new))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
