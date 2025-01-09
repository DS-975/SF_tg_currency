#pip install pytelegrambotapi

import telebot

from config import token, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(token)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message):
	text = ('Чтобы начать работу'
		'\nвведите команду боту в следующем формате :'
		'\n<имя валюты> <в какую валюту перевести > <количество переводимой валюты>'
		'\nДоступные валюты: /values')
	bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
	text = 'Доступные валюты :\n'
	for key in keys.keys():
		text = '\n'.join((text, key, ))
	bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
	try:
		values = message.text.split(' ')

		# Исключение, если пользователь ввёл не все 3 параметров
		if len(values) < 3:
			raise ConvertionException('Слишком мало параметров')
		elif len(values) > 3:
			raise ConvertionException('Слишком много параметров')

		# биткоин доллар 2
		quote, base, amount = values
		# Получаем от функции, которая получает данные о цене
		# с помощью запроса по апи, цену за 1 единицу
		total_base = CryptoConverter.get_price(quote, base, amount)

	except ConvertionException as e:
		bot.reply_to(message, f'Ошибка пользователя. \n{e}')
	except Exception as e:
		bot.reply_to(message, f'Не удалось обработать команду\n'
				      				f'{e}')
	else:
		text = f'Цена {amount} {quote} в {base} - {total_base}'
		bot.send_message(message.chat.id, text)

# Чтобы запустить бота, нужно воспользоваться методом polling
bot.polling(none_stop=True)
# Параметр none_stop говорит, что бот должен стараться
# не прекращать работу при возникновении каких либо ошибок
