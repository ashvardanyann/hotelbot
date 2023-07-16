from api import api_request

method_endswith_1 = 'locations/v3/search'
params_1 = {'q': 'Рига', 'locale': 'ru_RU'}
method_type_1 = 'GET'

response_1 = api_request(method_endswith=method_endswith_1, params=params_1, method_type=method_type_1)
print(response_1['sr'][0]['gaiaId'])
regionId = response_1['sr'][0]['gaiaId']

params_2 = {"currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {
                "regionId": regionId  # id из первого запроса
            },
            "checkInDate": {"day": 13, "month": 7, "year": 2023},
            "checkOutDate": {"day": 15, "month": 7, "year": 2023},
            "rooms": [{"adults": 1}],
            "resultsStartingIndex": 0,
            "resultsSize": 3,
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
            }

method_endswith_2 = 'properties/v2/list'
method_type_2 = 'POST'
response_2 = api_request(method_endswith=method_endswith_2, params=params_2, method_type=method_type_2)
# print(len(response_2['data']['propertySearch']['properties']))
# for i in response_2['data']['propertySearch']['properties']:
#    print(i['id'])

method_endswith_3 = 'properties/v2/detail'
method_type_3 = 'POST'
params_3 = {"currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "propertyId": response_2['data']['propertySearch']['properties'][0]['id']
            }
response_3 = api_request(method_endswith=method_endswith_3, params=params_3, method_type=method_type_3)
#print(response_3['data']['propertyInfo']['summary']['location']['address']['addressLine'])
print(response_3['data']['propertyInfo']['propertyGallery'])
