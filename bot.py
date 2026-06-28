import telebot
import time
import feedparser
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from urllib.parse import unquote

TOKEN = "8951072407:AAHP7oUUcfkDJ44SoDWkUgKyUwanBQocmuk"
ADMIN_ID = 7419211122
CHANNEL_ID = -1004414503790
CHANNEL = "https://t.me/novosti30reg"

bot = telebot.TeleBot(TOKEN)
user_names = {}
posted_news = set()

RSS_FEEDS = [
    "https://punkt-a.info/rss.xml",
    "https://astravolga.ru/feed/",
]

KEYWORDS = ["астрахань", "астраханск", "астраханцы", "волга", "астраханского", "астраханской"]

def is_astrakhan_news(title, summary=""):
    text = (title + " " + summary).lower()
    return any(word in text for word in KEYWORDS)

def check_news():
    while True:
        for feed_url in RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    title = entry.get("title", "")
                    link = unquote(entry.get("link", ""))
                    summary = entry.get("summary", "")

                    if link in posted_news:
                        continue

                    if not is_astrakhan_news(title, summary):
                        continue

                    posted_news.add(link)

                    text = (
                        f"🗞 *{title}*\n\n"
                        f"📍 Астрахань\n\n"
                        f"🔗 [Читать полностью]({link})"
                    )
                    bot.send_message(CHANNEL_ID, text, parse_mode="Markdown")
                    time.sleep(3)

            except Exception as e:
                print(f"Ошибка RSS: {e}")

        time.sleep(1800)

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
        f"Здесь ты можешь:\n"
        f"— Читать последние новости\n"
        f"— Написать в редакцию\n"
        f"— Узнать о канале\n\n"
        f"Выбери что тебя интересует 👇",
        parse_mode="Markdown",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📰 Последние новости")
def news(message):
    bot.send_message(message.chat.id,
        f"📰 Последние новости Астрахани:\n\n"
        f"Читай всё актуальное на нашем канале 👇\n\n"
        f"{CHANNEL}",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📢 О канале")
def about(message):
    bot.send_message(message.chat.id,
        f"📢 *Астрахань | Новости*\n\n"
        f"Главный новостной канал Астрахани.\n\n"
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
    msg = bot.send_message(message.chat.id,
        "Напиши своё имя и я буду обращаться к тебе по имени 😊")
    bot.register_next_step_handler(msg, save_name)

def save_name(message):
    user_names[message.chat.id] = message.text
    bot.send_message(message.chat.id,
        f"✅ Отлично, {message.text}! Теперь я знаю как тебя зовут 👋",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "📩 Написать в редакцию")
def ask_message(message):
    msg = bot.send_message(message.chat.id,
        "✍️ Напиши своё сообщение и я передам его в редакцию:")
    bot.register_next_step_handler(msg, forward_to_admin)

def forward_to_admin(message):
    name = user_names.get(message.chat.id, "Аноним")
    try:
        bot.send_message(ADMIN_ID,
            f"📩 Новое сообщение от {name} (@{message.from_user.username}):\n\n"
            f"{message.text}")
        bot.send_message(message.chat.id,
            "✅ Сообщение отправлено в редакцию! Спасибо.",
            reply_markup=main_menu())
    except Exception as e:
        print(f"Ошибка: {e}")

news_thread = threading.Thread(target=check_news)
news_thread.daemon = True
news_thread.start()

print("✅ Бот запущен!")
while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
