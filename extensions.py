import requests
import json
from config import keys

# Обрабатываем ошибки
class ConvertionException(Exception):
	pass

class CryptoConverter:
	@staticmethod
	def get_price(quote: str, base: str, amount: str):
		# Исключение, если пользователь ввел 2 одинаковые валюты
		if quote == base:
			raise ConvertionException(f'Невозможно перевести '
						  f'одинаковые валюты {base}.')

		# Обработчик ошибки, если пользователь вписал
		# неправильно параметр 1 валюты
		try:
			quote_ticker = keys[quote]
		except KeyError:
			raise ConvertionException(f'Не удалось обработать валюту '
						  f'{quote}')
		# Обработчик ошибки, если пользователь вписал
		# неправильно параметр 2 валюты
		try:
			base_ticker = keys[base]
		except KeyError:
			raise ConvertionException(f'Не удалось обработать валюту '
						  f'{base}')

		# Обработчик ошибки, если пользователь вписал
		# не в том формате параметр - количество
		try:
			amount = float(amount)
		except ValueError:
			raise ConvertionException(f'Не удалось обработать '
						  f'количество {amount}')

		# Получение данных о цене
		r = requests.get(
			f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
		# - ответ
		# print(r.content)
		#  Обращаемся к полученному объекту как к словарю и печатаем одно из значений
		total_base = json.loads(r.content)[keys[base]] * amount

		return total_base