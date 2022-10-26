import requests
import json


def get_info() -> list:
    data = []
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "9d5afc8b-c5ec-4948-a470-7764fcac06c1"
    }
    parameters = {"slug": "bitcoin", "convert": "USD"}
    response = requests.get(url, params=parameters, headers=headers)
    data.append(round(float(json.loads(response.text)["data"]["1"]["quote"]["USD"]["price"]), 1))
    parameters = {"slug": "ethereum", "convert": "USD"}
    response = requests.get(url, params=parameters, headers=headers)
    data.append(round(float(json.loads(response.text)["data"]["1027"]["quote"]["USD"]["price"]), 1))
    return data




