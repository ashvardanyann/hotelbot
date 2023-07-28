import requests

url = "https://hotels4.p.rapidapi.com/properties/v2/list"

payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {"regionId": "6054439"},
    "checkInDate": {
        "day": 29,
        "month": 7,
        "year": 2023
    },
    "checkOutDate": {
        "day": 31,
        "month": 7,
        "year": 2023
    },
    "rooms": [
        {
            "adults": 2,
            "children": [{"age": 5}, {"age": 7}]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 10,
    "sort": "PRICE_HIGH_TO_LOW",
    "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
}
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers).json()
data = response['data']['propertySearch']['properties']
data = sorted(data, key=lambda x: int(x['price']['lead']['formatted'][1:]), reverse=True)

for i in data:
    print(i['price']['lead']['formatted'], i['name'])



