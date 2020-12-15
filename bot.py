import os 
import telebot
import config
from flask import Flask, request
from buttons import button_url
from message import hellomessage, choose_message
from main import down_music, down_video


server = Flask(__name__)

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['help', 'start'])
def answer(message):
    bot.send_message(message.chat.id, hellomessage(message.chat.username))


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, choose_message, reply_markup=button_url(message.text))

@server.route("/", methods=["POST"])
def receive_update():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return {"ok": True}

@server.route('/' + config.token, methods=['POST'])
def getMessage():
    print("bot")
    bot.process_new_updates(
        [telebot.types.Update.de_json(
            request.stream.read().decode("utf-8"))])
    return "!", 200

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    if query.message.json['reply_markup']['inline_keyboard'][0][0]['text'] == 'audio':
        bot.send_message(
            query.message.chat.id,
            'Вы выбрали аудио, дождитесь загрузки')
        url = query.data
        down = down_music(url)
        bot.delete_message(query.message.chat.id, query.message.json['message_id'])
        audio = open(down, 'rb')
        bot.send_audio(query.message.chat.id, audio)
        os.remove(down)
    elif query.message.json['reply_markup']['inline_keyboard'][0][0]['text'] == 'video':
        bot.send_message(
            query.message.chat.id,
            'Вы выбрали видео, дождитесь загрузки')
        urlv = query.data
        downv = down_video(urlv)[1]
        bot.delete_message(query.message.chat.id, query.message.json['message_id'])
        video = open(downv, 'rb')
        bot.send_video(query.message.chat.id, video)
        os.remove(downv)


@bot.message_handler(content_types=["text"])
def delete_message(message):
    msg = bot.send_message(message.chat.id, 'Hello World')
    bot.edit_message_text("I AM Deleting Now",msg.chat_id,msg.message_id)
    bot.delete_message(message.chat.id, msg.message_id)


@server.route("/")
def webhook():
    print("bot")

    bot.remove_webhook()
    s = bot.set_webhook(
        url='https://b85369f278d0.ngrok.io' + config.token)
    if s:
        return print("webhook setup ok")
    else:
        return print("webhook setup failed")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


