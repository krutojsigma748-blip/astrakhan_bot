import telebot
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8951072407:AAHP7oUUcfkDJ44SoDWkUgKyUwanBQocmuk"
ADMIN_ID = 7419211122
CHANNEL = "https://t.me/novosti30reg"

bot = telebot.TeleBot(TOKEN)
user_names = {}

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("📰 Последние новости"))
    markup.add(KeyboardButton("📢 О канале"))
    markup.add(KeyboardButton("✏️ Указать имя"))
    markup.add(KeyboardButton("📩 Написать в редакцию"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    name = user_names.get(message.chat.id, "друг")
    bot.send_message(message.chat.id,
        f"👋 Привет, {name}!\n\n"
        f"Это бот канала *Астрахань | Новости* 🌊\n\n"
        f"Выбери что тебя интересует 👇",
        parse_mode="Markdown",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📰 Последние новости")
def news(message):
    bot.send_message(message.chat.id,
        f"📰 Последние новости:\n\n{CHANNEL}",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📢 О канале")
def about(message):
    bot.send_message(message.chat.id,
        f"📢 *Астрахань | Новости*\n\n"
        f"Публикуем:\n"
        f"🚨 Происшествия и ЧП\n"
        f"🏙 Городские новости\n"
        f"🌤 Погода и транспорт\n"
        f"🏛 Власть и экономика\n"
        f"🎉 Афиша и события\n\n"
        f"Подписывайся: {CHANNEL}",
        parse_mode="Markdown",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "✏️ Указать имя")
def ask_name(message):
    msg = bot.send_message(message.chat.id, "Напиши своё имя 😊")
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    user_names[message.chat.id] = message.text
    bot.send_message(message.chat.id,
        f"✅ Отлично, {message.text}! 👋",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📩 Написать в редакцию")
def ask_message(message):
    msg = bot.send_message(message.chat.id, "✍️ Напиши сообщение:")
    bot.register_next_step_handler(msg, forward_to_admin)

def forward_to_admin(message):
    name = user_names.get(message.chat.id, "Аноним")
    try:
        bot.send_message(ADMIN_ID,
            f"📩 От {name} (@{message.from_user.username}):\n\n{message.text}")
        bot.send_message(message.chat.id,
            "✅ Сообщение отправлено! Спасибо.",
            reply_markup=main_menu())
    except Exception as e:
        print(f"Ошибка: {e}")

print("✅ Бот запущен!")
while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
