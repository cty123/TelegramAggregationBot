from pyrogram import Client
from pyrogram.handlers import MessageHandler
from mongoengine import connect
import logging

from tgbot.adapter.handler import TGBotHandler 

logging.basicConfig(level = logging.INFO)

connect(host="mongodb+srv://mongodb URL here")

handler = MessageHandler(TGBotHandler().handle)

app = Client("bot_account", config_file="config.ini")
app.add_handler(handler)

logging.info("Starting running telegram bot")

app.run()
