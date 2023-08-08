from api import api_request
from requests import get

"""Функция для получения названий отелей и цен."""


def get_first_hotel_info(region: str,
                         results_size: str,
                         price_type: str,
                         check_in_date: str,
                         check_out_date: str,
                         adults: str,
                         children: str,
                         price_diopozon: str = None):
    day_in, month_in, year_in = check_in_date.split('-')
    day_out, month_out, year_out = check_out_date.split('-')

    response_1 = api_request(
        method_endswith='locations/v3/search',
        params={'q': region, 'locale': 'ru_RU'},
        method_type='GET')

    region_id = response_1['sr'][0]['gaiaId']
    params_2 = {"currency": "USD",
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "destination": {
                    "regionId": region_id  # id из первого запроса
                },
                "checkInDate": {"day": int(day_in), "month": int(month_in), "year": int(year_in)},
                "checkOutDate": {"day": int(day_out), "month": int(month_out), "year": int(year_out)},
                "rooms": [{"adults": int(adults)}],
                "resultsStartingIndex": 0,
                "resultsSize": int(results_size),
                "sort": "PRICE_LOW_TO_HIGH",
                "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
                }

    if children != 'Нет детей':
        params_2['rooms'][0]['children'] = [{'age': int(data)} for data in children.split(',')]

    response_2 = list()

    if price_type == "low":
        response_2 = api_request(method_endswith='properties/v2/list', params=params_2,
                                 method_type='POST')['data']['propertySearch']['properties']

    elif price_type == 'high':
        params_2['sort'] = 'PRICE_HIGH_TO_LOW'
        response_2 = api_request(method_endswith='properties/v2/list', params=params_2,
                                 method_type='POST')['data']['propertySearch']['properties']
        response_2 = sorted(response_2, key=lambda x: int(x['price']['lead']['formatted'][1:]), reverse=True)

    elif price_type == 'custom':
        price_min, price_max = price_diopozon.split('-')
        params_2['filters'] = {"price": {"max": int(price_max), "min": int(price_min)}}
        response_2 = api_request(method_endswith='properties/v2/list', params=params_2,
                                 method_type='POST')['data']['propertySearch']['properties']

    return [{'name': data['name'], 'hotel_id': data['id'], 'price': data['price']['lead']['formatted']} for data in
            response_2]


"""Функция для получения изображений и точного адреса определенного отеля."""


def get_second_hotel_info(hotel_id: str):
    params_3 = {"currency": "USD",
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "propertyId": hotel_id
                }
    response_3 = api_request(method_endswith='properties/v2/detail',
                             params=params_3,
                             method_type='POST')
    result = dict()
    result['address'] = response_3['data']['propertyInfo']['summary']['location']['address']['addressLine']
    result['photos'] = []
    photos_list = response_3['data']['propertyInfo']['propertyGallery']['images']
    for data in range(5):
        result['photos'].append(get(url=photos_list[data]['image']['url']).content)
    return result
