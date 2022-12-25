import requests
import json
from config import keys

class APIExeption(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise APIExeption(f'Невозможно перевести одинаковые валюты {base}.')
        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество {amount}.')


        quote_ticker, base_ticker = keys[quote], keys[base]
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base
