import telebot
from storage import TOKEN, currency
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    txt = ('Чтобы начать со мной работу введите:\n<наименование валюты> \
<её количество> \
<в какую валюту перевести>\n'
'Показать список доступных валют: /values\n'
'Справка: Я использую курсы криптовалют с сайта\n'
'https://www.cryptocompare.com')
    bot.reply_to(message, txt)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    txt = 'Доступные валюты'
    for key in currency.keys():
        txt = '\n'.join((txt, key, ))
    bot.reply_to(message, txt)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise APIException('Для запроса конвертации нужны ТРИ параметра')

        quote, amount, base = value
        total_base = Converter.get_price(quote, amount, base)
    except APIException as e:
        bot.reply_to(message, f'Ошибка!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {quote} = {round(total_base * float(amount), 2)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()