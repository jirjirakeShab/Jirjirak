import telebot
from telebot import types

API_TOKEN = '7803977509:AAFw9SYsltcp3OHbpc-3Odlfgv86NKW-SJo'
REQUIRED_CHANNELS = ['@masaloya', '@LaSillage']

bot = telebot.TeleBot(API_TOKEN)

def check_membership(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            # وضعیت های مجاز که عضو حساب میشه
            if member.status not in ['member', 'creator', 'administrator']:
                return False
        except Exception as e:
            print(f"Error checking membership for {channel}: {e}")
            return False
    return True

def generate_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📥 Masaloya", url="https://t.me/masaloya"),
        types.InlineKeyboardButton("🌫 La Sillage", url="https://t.me/LaSillage")
    )
    markup.add(types.InlineKeyboardButton("🔁 بررسی عضویت", callback_data="check"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "جیرجیرک شب‌بیدار | فیلمای داغ ❤️‍🔥\n"
        "اگه زیر 18 سالی نیااا :/\n\n"
        "📌 برای ورود به فضای خصوصی ما، اول باید عضو دو کانال زیر باشی:\n\n"
        "1️⃣ @masaloya\n"
        "2️⃣ @LaSillage\n\n"
        "وقتی عضو شدی، روی دکمه‌ی زیر بزن:\n👇👇👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=generate_markup())

@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id
    if check_membership(user_id):
        bot.answer_callback_query(call.id, "✅ عضویتت تایید شد!")
        # اینجا فیلم رو میفرستی، مثلا نمونه:
        video_link = "https://t.me/masaloya/123"  # لینک فیلم یا پیام کانال فیلم
        bot.send_message(call.message.chat.id, f"🔥 خوش اومدی! اینم فیلم مخصوصت:\n{video_link}")
    else:
        bot.answer_callback_query(call.id, "⛔ هنوز عضو نشدی!")
        bot.send_message(call.message.chat.id,
                         "هنوز عضو هر دو کانال نیستی!\nلطفاً اول عضو شو بعد روی دکمه بررسی بزن.",
                         reply_markup=generate_markup())

bot.infinity_polling()