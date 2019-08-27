import telebot
from telebot import apihelper
import requests
import random


apihelper.proxy = {'https': 'socks5h://382210467:yJD0LQSj@orbtl.s5.opennetwork.cc:999'}

TOKEN = '927573390:AAEdFSK1j5Q6_n_WRjV7OHYHzgalY7tPN0c'
YOUTUBE_KEY = 'AIzaSyCccZT5OAsd_Hio2N8JREeaQP8lytS5C5I'

bot = telebot.TeleBot(TOKEN)

allowed_users = ['lapsha666']


@bot.message_handler(content_types=['text'])
def get_text_message(message):
	username = message.from_user.username
	if message.text.lower().startswith('щегол'):
		youtube_video(message, username)
	elif 'подтверди щегол' in message.text.lower():
		yes_my_lord(message, username)


def youtube_video(message, username):

	video = message.text.lower().split('щегол')[-1]
	if len(video) != 0:
		youtube_searcher = requests.get('https://www.googleapis.com/youtube/v3/search', params={
			'key': YOUTUBE_KEY,
			'part': ['snippet'],
			'q': '{}'.format(video)})
		video_id = youtube_searcher.json()['items'][0]['id']['videoId']
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id,
						 'Не благодари, петух. \n https://www.youtube.com/watch?v={}'.format(video_id))
	else:
		bot.send_message(message.chat.id,
						 'Сам ты щегол @{}, введи нормальный запрос: "Щегол <название видео>".'.format(username))


def yes_my_lord(message, username):
	if username in allowed_users:
		bot.reply_to(message, str(random.choice(['Поистине великолепная мысль @{}, впрочем как и всегда!',
												'Я поражаюсь твоему интеллекту @{}!',
												'Зачем @{} ты что-то доказываешь этим холопам?'])).format(username))
	else:
		bot.reply_to(message, 'Ничего не буду подтверждать. Не стоит спорить с барином.')


if __name__ == '__main__':
	bot.polling(none_stop=True, interval=0)