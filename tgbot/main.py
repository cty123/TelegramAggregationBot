import configparser
import argparse
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from mongoengine import connect
import logging

from tgbot.adapter.handler import TGBotHandler

LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
DEFAULT_CONFIG_PATH = './config.ini'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)

    # Parse arguments
    # Optional arguments:
    #  -h, --help: See all the available options
    #  -c, --config: The configuration file that the program should read from
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', nargs=1, help='the configuration ini file that the program should read from. '
                                                        'Default to ./config.ini')
    args = parser.parse_args()
    config_path = args.config if args.config else DEFAULT_CONFIG_PATH

    # Parse configuration
    config = configparser.ConfigParser()
    config.read(config_path)

    # Read configuration
    api_id = config["pyrogram"]["api_id"]
    api_hash = config["pyrogram"]["api_hash"]
    mongodb_url = config["MediaAggregator"]["mongodb"]
    bot_token = config["Telegram"]["bot_token"]

    # Connect data base
    connect(host=mongodb_url)

    handler = MessageHandler(TGBotHandler().handle)

    app = Client("bot_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
    app.add_handler(handler)

    logging.info("Starting running telegram bot")

    app.run()
