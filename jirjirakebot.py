import telebot
from telebot import types

API_TOKEN = '7803977509:AAFw9SYsltcp3OHbpc-3Odlfgv86NKW-SJo'
REQUIRED_CHANNELS = ['@masaloya', '@LaSillage']  # لیست کانال‌هایی که باید عضو باشند

bot = telebot.TeleBot(API_TOKEN)

# بررسی عضویت در همه کانال‌ها
def check_membership(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'creator', 'administrator']:
                return False
        except:
            return False
    return True

# دکمه‌ها
def generate_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📥 Masaloya", url="https://t.me/masaloya"),
        types.InlineKeyboardButton("🌫 La Sillage", url="https://t.me/LaSillage")
    )
    markup.add(types.InlineKeyboardButton("🔁 بررسی عضویت", callback_data="check"))
    return markup

# استارت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """جیرجیرک شب‌بیدار | فیلمای داغ ❤️‍🔥
اگه زیر 18 سالی نیااا :/

📌 برای ورود به فضای خصوصی ما، اول باید عضو دو کانال زیر باشی:

1️⃣ @masaloya
2️⃣ @LaSillage

وقتی عضو شدی، روی دکمه‌ی زیر بزن:
👇👇👇"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=generate_markup())

# بررسی عضویت وقتی روی دکمه کلیک می‌کنن
@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id
    if check_membership(user_id):
        bot.answer_callback_query(call.id, "✅ عضویتت تایید شد!")
        bot.send_message(call.message.chat.id, "🔥 خوش اومدی! حالا می‌تونی فیلمای داغ جیرجیرک شب رو ببینی...")
    else:
        bot.answer_callback_query(call.id, "⛔ هنوز عضو نشدی!")
        bot.send_message(call.message.chat.id, "هنوز عضو هر دو کانال نیستی!\nلطفاً اول عضو شو بعد روی دکمه بررسی بزن.", reply_markup=generate_markup())

bot.infinity_polling()
