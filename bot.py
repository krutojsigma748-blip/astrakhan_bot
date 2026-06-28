import telebot
import time

TOKEN = "8951072407:AAHP7oUUcfkDJ44SoDWkUgKyUwanBQocmuk"
ADMIN_ID = 7419211122

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def forward_to_admin(message):
    if message.chat.id != ADMIN_ID:
        try:
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "✅ Ваше сообщение получено! Спасибо.")
        except Exception as e:
            print(f"Ошибка пересылки: {e}")

print("✅ Бот запущен!")
while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
