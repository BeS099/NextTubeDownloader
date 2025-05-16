import os
import telebot
from telebot import types
import yt_dlp

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلًا بيك في بوت تحميل يوتيوب! أرسل رابط فيديو وسأعطيك خيارات التحميل.")

@bot.message_handler(func=lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
def handle_youtube_link(message):
    url = message.text
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("تحميل فيديو", callback_data=f"video|{url}")
    btn2 = types.InlineKeyboardButton("تحميل صوت", callback_data=f"audio|{url}")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "شنو تريد تحمل؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data, url = call.data.split("|")
    chat_id = call.message.chat.id

    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestaudio/best' if data == "audio" else 'best',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        with open(file_name, 'rb') as f:
            if data == "audio":
                bot.send_audio(chat_id, f)
            else:
                bot.send_video(chat_id, f)

        os.remove(file_name)

    except Exception as e:
        bot.send_message(chat_id, f"حدث خطأ أثناء التحميل: {e}")

bot.polling()
