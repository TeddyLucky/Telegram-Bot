import telebot
from config import TOKEN, CURRENCIES
from extensions import APIException, CurrencyConverter

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)


# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    instructions = '''
💰 *Конвертер валют* 💰

Чтобы узнать цену валюты, отправьте сообщение в формате:
`<имя валюты> <имя валюты для перевода> <количество>`

Например:
`доллар рубль 100` - узнать стоимость 100 долларов в рублях

Доступные команды:
/values - список доступных валют
/help - инструкция по использованию бота
    '''
    bot.send_message(message.chat.id, instructions, parse_mode='Markdown')


# Обработчик команды /values
@bot.message_handler(commands=['values'])
def handle_values(message):
    available_currencies = '*Доступные валюты:*\n'
    for key in CURRENCIES.keys():
        available_currencies += f'- {key.capitalize()} ({CURRENCIES[key]})\n'
    bot.send_message(message.chat.id, available_currencies, parse_mode='Markdown')


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_conversion(message):
    try:
        # Разбиение сообщения на параметры
        params = message.text.strip().split()

        if len(params) != 3:
            raise APIException(
                'Неверный формат ввода. Используйте формат: <имя валюты> <имя валюты для перевода> <количество>')

        base, quote, amount = params
        result = CurrencyConverter.get_price(base, quote, amount)

        # Форматирование сообщения с результатом
        base_code = CURRENCIES.get(base.lower(), base.upper())
        quote_code = CURRENCIES.get(quote.lower(), quote.upper())
        response = f'{amount} {base_code} = {result} {quote_code}'

        bot.send_message(message.chat.id, response)

    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка ввода: {str(e)}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла системная ошибка: {str(e)}')


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

