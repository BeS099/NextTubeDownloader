
import os
import telebot
from pytube import YouTube
from telebot import types

TOKEN = TOKEN = "7948704852:AAF6taVJa2NgYgxjp02GfgolTKx5x4DiXL4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلًا بيك في بوت تحميل يوتيوب!\nأرسل رابط فيديو من يوتيوب وسأعطيك خيارات التحميل.")

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
        yt = YouTube(url)
        if data == "video":
            bot.send_message(chat_id, "جاري تحميل الفيديو...")
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        else:
            bot.send_message(chat_id, "جاري تحميل الصوت...")
            stream = yt.streams.filter(only_audio=True).first()

        file_path = stream.download(filename_prefix="nexttube_")
        with open(file_path, 'rb') as f:
            if data == "video":
                bot.send_video(chat_id, f)
            else:
                bot.send_audio(chat_id, f)

        os.remove(file_path)
    except Exception as e:
        bot.send_message(chat_id, f"حدث خطأ: {e}")

bot.polling()
