import logging
import random

from backports.configparser import ConfigParser
from telegram.ext import Updater, CommandHandler

from bot_messages import get_product_promotion_message
from telegram_aliexpress_bot.aliexpress_api import AliExpressApi

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
aliexpress_api = AliExpressApi()


# todo: implement properly, with "next" functionality
def promo(bot, update):
    data = aliexpress_api.get_hot_products()

    result_count = data["result"]["totalResults"]
    random_result_index = random.randint(0, result_count - 1)

    bot.send_photo(chat_id=update.message.chat_id,
                   photo=data["result"]["products"][random_result_index]["imageUrl"],
                   message_id=update.message.message_id)


# todo: implement
def search(bot, update, args):
    print(args)
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=args[0],
                   message_id=update.message.message_id)


def link(bot, update, args):
    product_url = args[0]
    product_details = aliexpress_api.get_promotion_product_detail_from_link(product_url)

    # todo: create data class for these api results...
    image_url = product_details['result']['imageUrl']
    product_url = product_details['result']['productUrl']
    product_title = product_details['result']['productTitle']
    product_price = product_details['result']['salePrice']

    bot.send_photo(chat_id=update.message.chat_id,
                   message_id=update.message.message_id,
                   photo=image_url,
                   caption=get_product_promotion_message(product_title, product_price, product_url)
                   )


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

    # todo: build a menu and conversation handler
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
