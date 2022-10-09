import telebot
from os import getenv
from core.settings import ENV

bot = telebot.TeleBot(ENV.get('BOT_TOKEN'))


def send_welcome(message):
    bot.send_message(message,
        "Hi there, I am EchoBot. I am here to echo your kind words back to you. Just say anything nice and Ill say the exact same thing to you!"
    )


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
