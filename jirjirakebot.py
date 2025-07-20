import telebot
from telebot import types
import json

API_TOKEN = '7803977509:AAFw9SYsltcp3OHbpc-3Odlfgv86NKW-SJo'
REQUIRED_CHANNELS = ['@masaloya', '@LaSillage']

bot = telebot.TeleBot(API_TOKEN)

with open('videos.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

def check_membership(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'creator', 'administrator']:
                return False
        except:
            return False
    return True

def generate_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📥 Join @masaloya", url="https://t.me/masaloya"),
        types.InlineKeyboardButton("🌫 Join @LaSillage", url="https://t.me/LaSillage")
    )
    return markup

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1:
        requested_message_id = int(args[1])
        video = None
        for v in videos:
            if v['message_id'] == requested_message_id:
                video = v
                break
        if not video:
            bot.send_message(message.chat.id, "❌ فیلم یافت نشد.")
            return

        if check_membership(user_id):
            try:
                bot.forward_message(message.chat.id, video['channel_id'], video['message_id'])
            except Exception as e:
                bot.send_message(message.chat.id, "خطایی رخ داد، لطفا بعداً تلاش کن.")
        else:
            text = ("🎥 برای دریافت فیلم باید عضو کانال‌های زیر شوی:\n"
                    "1️⃣ @masaloya\n"
                    "2️⃣ @LaSillage\n\n"
                    "بعد از جوین، دوباره استارت بزن.")
            bot.send_message(message.chat.id, text, reply_markup=generate_markup())
    else:
        text = ("سلام! برای دریافت فیلم، لطفاً روی لینک مخصوص هر فیلم تو کانال کلیک کن.")
        bot.send_message(message.chat.id, text)

bot.infinity_polling()
