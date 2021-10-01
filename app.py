import telebot
from config import keys, TOKEN
from extentions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Я - бот-конвертер.\nПомогу Вам перевести одну валюту в другую по актуальному на текущий момент курсу.\n\n\
Чтобы начать работу, введите сообщение в следующем формате:\n\
<имя переводимой валюты>\n<в какую валюту перевести>\n<количество переводимой валюты>\n\
Например: евро доллар 15\n\nВы можете управлять мной, посылая эти команды:\n\
/values - список доступных валют\n/help - помощь'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} составляет {total_base} {quote}'
        bot.send_message(message.chat.id, text)

bot.polling()