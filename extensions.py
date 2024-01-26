import requests
import json
from storage import currency

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, amount: str, base:str):

        if quote == base:
            raise APIException('Одинаковые валюты')

        try:
            first = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            second = currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {base}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={first}&tsyms={second}')
        total_base = json.loads(r.content)[second]

        return total_base