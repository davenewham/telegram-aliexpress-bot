#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.

# This program is dedicated to the public domain under the CC0 license.
"""
import logging
import random

from backports.configparser import SafeConfigParser, ConfigParser
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from telegram_aliexpress_bot.aliexpress_api import AliExpressApi

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
aliexpress_api = AliExpressApi()


def promo(bot, update):
    query = update
    data = aliexpress_api.get_hot_products()

    result_count = data["result"]["totalResults"]
    random_result_index = random.randint(0, result_count - 1)

    bot.send_photo(chat_id=query.message.chat_id,
                   photo=data["result"]["products"][random_result_index]["imageUrl"],
                   message_id=query.message.message_id)


def search(bot, update, args):
    print(args)
    query = update
    bot.send_photo(chat_id=query.message.chat_id,
                   photo=args[0],
                   message_id=query.message.message_id)


def link(bot, update, args):
    pass


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Import api key
    parser = ConfigParser()
    parser.read('config.ini')
    bot_token = parser.get('Telegram', 'token')

    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_token)

    updater.dispatcher.add_handler(CommandHandler('promo', promo))
    updater.dispatcher.add_handler(CommandHandler('search', search, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('link', link, pass_args=True))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
