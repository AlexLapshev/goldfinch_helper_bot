import telebot
import requests
import random
from PIL import Image
from io import BytesIO


TOKEN = ''
YOUTUBE_KEY = ''

bot = telebot.TeleBot(TOKEN)

photo_download_link = 'https://api.telegram.org/file/bot{}/'.format(TOKEN)

allowed_users = ['lapsha666']


@bot.message_handler(content_types=['text', 'photo'])
def get_text_message(message):
	username = message.from_user.username

	if message.content_type == 'text':
		if message.text.lower().startswith('щегол'):
			youtube_video(message, username)
		elif 'подтверди щегол' in message.text.lower():
			yes_my_lord(message, username)
	elif message.content_type == 'photo' and message.caption:
		if message.caption.lower() == 'щегол':
			combining_image(message)


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
						 'Не благодари. \n https://www.youtube.com/watch?v={}'.format(video_id))
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


def combining_image(message):
	photo_id = message.json['photo'][-1]['file_id']
	photo_link = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(TOKEN, photo_id)
	file_path = requests.get(photo_link).json()['result']['file_path']

	full_path = 'https://api.telegram.org/file/bot{}/{}'.format(TOKEN, file_path)
	img = requests.get(full_path)
	background = Image.open(BytesIO(img.content))
	width = background.size[1] // 3
	size = (width, width)
	foreground = Image.open('images/shlem_LOGO_white_with_texture.png')
	foreground = foreground.resize(size, Image.ANTIALIAS)
	background.paste(foreground, (0, 0), foreground)

	img_byte_arr = BytesIO()
	background.save(img_byte_arr, format='JPEG')
	img_byte_arr = img_byte_arr.getvalue()

	bot.delete_message(message.chat.id, message.message_id)
	bot.send_photo(message.chat.id, img_byte_arr)


if __name__ == '__main__':
	bot.polling(none_stop=True, interval=0)