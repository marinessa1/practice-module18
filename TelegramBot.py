import telebot
from config import keys, TOKEN
from extensions import APIExeption, Converter
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Приветствую,  {message.chat.username}!\n\n"
                                      f"Чтобы узнать стоимость интересующей Вас валюты, введите команду в следующем формате:\n\n"
                                      f"<Наименование валюты цену которой необходимо узнать> <Наименование валюты в которой необходимо узнать цену> <Количество валюты> (например, доллар рубль 2)\n"
                                      f"Список доступных валют можно узнать по команде /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = f'Доступные валюты для перевода:'

    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIExeption('Слишком много параметров.')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)

    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()


