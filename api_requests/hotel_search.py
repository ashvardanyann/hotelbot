from api import api_request

# method_endswith_3 = 'properties/v2/detail'
# method_type_3 = 'POST'
# params_3 = {"currency": "USD",
#             "eapid": 1,
#             "locale": "ru_RU",
#             "siteId": 300000001,
#             "propertyId": response_2['data']['propertySearch']['properties'][0]['id']
#             }
# response_3 = api_request(method_endswith=method_endswith_3, params=params_3, method_type=method_type_3)
# #print(response_3['data']['propertyInfo']['summary']['location']['address']['addressLine'])
# print(response_3['data']['propertyInfo']['propertyGallery'])

def get_first_hotel_info(region: str,
                         results_size: int,
                         price_type: str,
                         check_in_date: str,
                         check_out_date: str,
                         adults: int,
                         children: str):

    day_in, month_in, year_in = check_in_date.split('-')
    day_out, month_out, year_out = check_out_date.split('-')


    response_1 = api_request(
        method_endswith='locations/v3/search',
        params={'q': region, 'locale': 'ru_RU'},
        method_type='GET')
#    print(response_1['sr'][0]['gaiaId'])
    regionId = response_1['sr'][0]['gaiaId']

    if price_type == "low":
        params_2 = {"currency": "USD",
                    "eapid": 1,
                    "locale": "ru_RU",
                    "siteId": 300000001,
                    "destination": {
                        "regionId": regionId  # id из первого запроса
                    },
                    "checkInDate": {"day": int(day_in), "month": int(month_in), "year": int(year_in)},
                    "checkOutDate": {"day": int(day_out), "month": int(month_out), "year": int(year_out)},
                    "rooms": [{"adults": adults,
                               "children": [{'age': int(i)} for i in children.split(',')]}],
                    "resultsStartingIndex": 0,
                    "resultsSize": results_size,
                    "sort": "PRICE_LOW_TO_HIGH",
                    "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
                    }
        response_2 = api_request(method_endswith='properties/v2/list', params=params_2, method_type='POST')
        return [{'name':data['name'], 'hotel_id': data['id'], 'price': data['price']['lead']['formatted']} for data in response_2['data']['propertySearch']['properties']]
        # return response_2


