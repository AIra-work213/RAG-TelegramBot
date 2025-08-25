from telebot import TeleBot
import os
import requests
import time
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
model = AutoModelForCausalLM.from_pretrained("model_name")

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256
)

llm = HuggingFacePipeline(pipeline=pipe)


bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    raise ValueError("BOT_TOKEN environment variable is not set.")
bot = TeleBot(bot_token)

'''Основные команды'''
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот для поиска информации в векторной базе данных. /search для выполнения поиска и /add для добавления сайта с текстом")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Я могу помочь вам найти информацию в векторной базе данных. Для этого вам нужно отправить мне сообщение с запросом.")

'''Поиск в БД'''
@bot.message_handler(commands=["search"])
def search(message):
    bot.send_message(message.chat.id, "Введите ваш запрос:")
    bot.register_next_step_handler(message, search_handler)

def search_handler(message):
    query = message.text
    for _ in range(5):
        try:
            response = requests.get(f"http://chroma_server:8000/search?query={query}")
            bot.send_message(message.chat.id, str(response.json())[:4000])
            return 1
        except requests.exceptions.ConnectionError:
            time.sleep(2)
    bot.send_message(message.chat.id, "Сервис поиска временно недоступен. Попробуйте позже.")


'''Добавление ссылки пользователя в векторную БД'''
@bot.message_handler(commands=["add"])
def add(message):
    bot.send_message(message.chat.id, "Введите URL сайта:")
    bot.register_next_step_handler(message, add_handler)

def add_handler(message):
    url = message.text
    for _ in range(3):
        try:
            response = requests.post(f"http://chroma_server:8000/add?url={url}")
            bot.send_message(message.chat.id, str(response.json()))
            return
        except requests.exceptions.ConnectionError:
            time.sleep(2)
    bot.send_message(message.chat.id, "Сервис добавления временно недоступен. Попробуйте позже.")

bot.polling()