from telebot import TeleBot
from env import Bot_token
import requests

bot = TeleBot(Bot_token)

'''Основные команды'''
@bot.message_handler(commands=["start"])
async def start(message):
    bot.send_message(message.chat.id, "Привет, я бот для поиска информации в векторной базе данных. /search для выполнения поиска и /add для добавления сайта с текстом")

@bot.message_handler(commands=["help"])
async def help(message):
    bot.send_message(message.chat.id, "Я могу помочь вам найти информацию в векторной базе данных. Для этого вам нужно отправить мне сообщение с запросом.")

'''Поиск'''
@bot.message_handler(commands=["search"])
async def search(message):
    bot.send_message(message.chat.id, "Введите ваш запрос:")
    bot.register_next_step_handler(message, search_handler)

async def search_handler(message):
    query = message.text
    response = requests.get(f"http://localhost:8000/search?query={query}")
    bot.send_message(message.chat.id, response.json())

'''Добавление ссылки пользователя в векторную БД'''
@bot.message_handler(commands=["add"])
async def add(message):
    bot.send_message(message.chat.id, "Введите URL сайта:")
    bot.register_next_step_handler(message, add_handler)

async def add_handler(message):
    url = message.text
    response = requests.post(f"http://localhost:8000/add?url={url}")
    bot.send_message(message.chat.id, response.json())

bot.polling()