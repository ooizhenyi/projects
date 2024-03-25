from dotenv import load_dotenv
import os
import telebot

dotenv_path = 'settings.env'
load_dotenv(dotenv_path)

token = os.getenv("BOT_TOKEN")

if token is None:
    print("Error: BOT_TOKEN environment variable not found.")
    exit()
else:
    print("BOT_TOKEN:", token)

bot = telebot.TeleBot(token)

#to handle incoming /message
@bot.message_handler(commands=['start', 'hello']) 
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    
#echoes all incoming text messages back to the sender
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
bot.infinity_polling()