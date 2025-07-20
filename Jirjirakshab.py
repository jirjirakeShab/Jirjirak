import telebot
from telebot import types

API_TOKEN = '7803977509:AAFw9SYsltcp3OHbpc-3Odlfgv86NKW-SJo'
REQUIRED_CHANNELS = ['@masaloya', '@LaSillage']

# اینجا پیام‌ها رو توی لیست تعریف کردم طبق آیدی کانال و مسیج‌هایی که دادی
MESSAGES = [
    {"channel_id": -1002855662383, "message_id": 2},
    {"channel_id": -1002855662383, "message_id": 3},
    {"channel_id": -1002855662383, "message_id": 4},
    {"channel_id": -1002855662383, "message_id": 5},
    {"channel_id": -1002855662383, "message_id": 6},
    {"channel_id": -1002855662383, "message_id": 7},
    {"channel_id": -1002855662383, "message_id": 8},
    {"channel_id": -1002855662383, "message_id": 9},
    {"channel_id": -1002855662383, "message_id": 10},
    {"channel_id": -1002855662383, "message_id": 11},
    {"channel_id": -1002855662383, "message_id": 12},
    {"channel_id": -1002855662383, "message_id": 13},
    {"channel_id": -1002855662383, "message_id": 14},
    {"channel_id": -1002855662383, "message_id": 15},
    {"channel_id": -1002855662383, "message_id": 16},
    {"channel_id": -1002855662383, "message_id": 17},
    {"channel_id": -1002855662383, "message_id": 18},
    {"channel_id": -1002855662383, "message_id": 19},
    {"channel_id": -1002855662383, "message_id": 20},
    {"channel_id": -1002855662383, "message_id": 21},
    {"channel_id": -1002855662383, "message_id": 22},
    {"channel_id": -1002855662383, "message_id": 23},
    {"channel_id": -1002855662383, "message_id": 24},
    {"channel_id": -1002855662383, "message_id": 25},
    {"channel_id": -1002855662383, "message_id": 26},
    {"channel_id": -1002855662383, "message_id": 27},
    {"channel_id": -1002855662383, "message_id": 28},
    {"channel_id": -1002855662383, "message_id": 29},
    {"channel_id": -1002855662383, "message_id": 30},
    {"channel_id": -1002855662383, "message_id": 31},
    {"channel_id": -1002855662383, "message_id": 32},
    {"channel_id": -1002855662383, "message_id": 33},
    {"channel_id": -1002855662383, "message_id": 34},
    {"channel_id": -1002855662383, "message_id": 35},
    {"channel_id": -1002855662383, "message_id": 36},
    {"channel_id": -1002855662383, "message_id": 37},
    {"channel_id": -1002855662383, "message_id": 38},
    {"channel_id": -1002855662383, "message_id": 39},
    {"channel_id": -1002855662383, "message_id": 40},
    {"channel_id": -1002855662383, "message_id": 41},
    {"channel_id": -1002855662383, "message_id": 42},
    {"channel_id": -1002855662383, "message_id": 43},
    {"channel_id": -1002855662383, "message_id": 44},
    {"channel_id": -1002855662383, "message_id": 45},
    {"channel_id": -1002855662383, "message_id": 46},
    {"channel_id": -1002855662383, "message_id": 47},
    {"channel_id": -1002855662383, "message_id": 48},
    {"channel_id": -1002855662383, "message_id": 49},
    {"channel_id": -1002855662383, "message_id": 50},
    {"channel_id": -1002855662383, "message_id": 51},
    {"channel_id": -1002855662383, "message_id": 52},
    {"channel_id": -1002855662383, "message_id": 53},
    {"channel_id": -1002855662383, "message_id": 54}
]

bot = telebot.TeleBot(API_TOKEN)

# تابع چک کردن عضویت در همه کانال‌ها
def check_membership(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            print(f"Error checking membership for {channel}: {e}")
            return False
    return True

# دکمه‌ها برای ورود به کانال‌ها و بررسی عضویت
def generate_markup():
    markup = types.InlineKeyboardMarkup()
    for ch in REQUIRED_CHANNELS:
        markup.add(types.InlineKeyboardButton(f"📥 {ch}", url=f"https://t.me/{ch[1:]}"))
    markup.add(types.InlineKeyboardButton("🔁 بررسی عضویت", callback_data="check"))
    return markup

# پیام شروع
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "سلام! برای دیدن فیلم‌های داغ جیرجیرک باید اول عضو کانال‌های زیر باشی:\n\n"
    )
    for ch in REQUIRED_CHANNELS:
        text += f"{ch}\n"
    text += "\nبعد از عضویت روی دکمه‌ی بررسی عضویت بزن."
    bot.send_message(message.chat.id, text, reply_markup=generate_markup())

# وقتی کاربر دکمه بررسی رو زد
@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id
    if check_membership(user_id):
        bot.answer_callback_query(call.id, "✅ عضویت تایید شد!")
        # ارسال چند پیام فیلم به ترتیب
        for msg in MESSAGES:
            try:
                bot.copy_message(chat_id=call.message.chat.id,
                                 from_chat_id=msg["channel_id"],
                                 message_id=msg["message_id"])
            except Exception as e:
                print(f"Error sending message {msg['message_id']} from channel {msg['channel_id']}: {e}")
        bot.send_message(call.message.chat.id, "🎬 همه فیلم‌ها فرستاده شد! لذت ببر ❤️")
    else:
        bot.answer_callback_query(call.id, "⛔ هنوز عضو کانال‌ها نیستی!")
        bot.send_message(call.message.chat.id, "لطفاً اول عضو کانال‌ها شو، سپس دوباره بررسی کن.", reply_markup=generate_markup())

bot.infinity_polling()