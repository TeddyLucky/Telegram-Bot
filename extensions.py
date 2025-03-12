import requests
import json
from config import CURRENCIES

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        """
        Метод для получения суммы конвертации валюты
        :param base: имя валюты, цену которой надо узнать
        :param quote: имя валюты, в которой надо узнать цену первой валюты
        :param amount: количество конвертируемой валюты
        :return: сумма в целевой валюте
        """
        # Проверка правильности ввода валют
        if base == quote:
            raise APIException('Невозможно конвертировать одинаковые валюты')
        
        try:
            base_code = CURRENCIES[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена. Используйте команду /values для просмотра доступных валют')
        
        try:
            quote_code = CURRENCIES[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена. Используйте команду /values для просмотра доступных валют')
        
        # Проверка правильности ввода суммы
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}. Введите корректное число')
        
        if amount <= 0:
            raise APIException('Количество валюты должно быть положительным числом')
        
        # Запрос к API для получения курса валют
        try:
            url = f'https://api.exchangerate-api.com/v4/latest/{base_code}'
            response = requests.get(url)
            data = json.loads(response.content)
            
            if response.status_code != 200:
                raise APIException(f'Ошибка API: {data.get("error", "Неизвестная ошибка")}')
            
            rate = data['rates'].get(quote_code)
            if rate is None:
                raise APIException(f'Не удалось получить курс для валюты {quote}')
            
            # Вычисление результата конвертации
            result = round(amount * rate, 2)
            return result
        except requests.exceptions.RequestException:
            raise APIException('Ошибка при обращении к сервису курсов валют. Пожалуйста, попробуйте позже')
  
