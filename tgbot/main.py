import configparser
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from mongoengine import connect
import logging

from tgbot.adapter.handler import TGBotHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config["pyrogram"]["api_id"]
api_hash = config["pyrogram"]["api_hash"]
mongodb_url = config["MediaAggregator"]["mongodb"]

connect(host=mongodb_url)

handler = MessageHandler(TGBotHandler().handle)

app = Client("bot_account", api_id=api_id, api_hash=api_hash)
app.add_handler(handler)

logging.info("Starting running telegram bot")

app.run()
