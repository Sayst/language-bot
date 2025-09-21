from config import token
import telebot
import requests

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для перевода текста. Для начала работы отправьте команду /setlang_to")


@bot.message_handler(commands=['setlang_to'])
def set_lang_to(message):
    msg = bot.send_message(message.chat.id, "Введите язык, на который нужно перевести (например, 'en' или 'ru')")
    bot.register_next_step_handler(msg, save_lang_to)

def save_lang_to(message):
    global lang_to
    lang_to = message.text.strip()
    bot.send_message(message.chat.id, f'Язык перевода установлен: {lang_to}\nТеперь отправьте команду /translate для перевода текста.')

@bot.message_handler(commands=['translate'])
def translate(message):
    msg = bot.send_message(message.chat.id, "Введите текст для перевода")
    bot.register_next_step_handler(msg, translate_text)

def translate_text(message):
    global sentence
    sentence = message.text.strip()
    bot.send_message(message.chat.id, "Перевожу...")
    url = "https://apifreellm.com/api/chat"
    headers = {
    "Content-Type": "application/json"
    }
    data = {
    "message": f"translate this sentence {sentence} to {lang_to} and return only translation"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()['response']
        bot.send_message(message.chat.id, f'Перевод:\n{result}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

if __name__ == "__main__":
    bot.polling(none_stop=True)