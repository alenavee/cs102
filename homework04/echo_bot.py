import telebot
from config import token

access_token = token
bot = telebot.TeleBot(access_token)
telebot.apihelper.proxy = {'https': 'https://51.38.71.101:8080'}


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling()