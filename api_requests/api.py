import requests
from loader import RAPID_API_KEY
from logger_dir import logger


def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    """Универсальная функция для отправки запросов к hotels4.p.rapidapi.com"""
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    # В зависимости от типа запроса вызываем соответствующую функцию
    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    else:
        return post_request(
            url=url,
            params=params
        )


def get_request(url, params):
    """Функция для отправки 'GET' запроса."""
    try:
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )

        if response.status_code == requests.codes.ok:
            return response.json()
    except Exception as e:
        logger.error(e)
        return None


def post_request(url, params):
    """Функция для отправки 'POST' запроса."""
    try:
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.post(
            url=url,
            json=params,
            headers=headers,
            timeout=15
        )

        if response.status_code == requests.codes.ok:
            return response.json()

    except Exception as e:
        logger.error(e)
        return None
