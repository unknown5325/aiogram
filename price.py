import requests


def byn_to_other():
    try:
        response = requests.get('https://open.er-api.com/v6/latest/byn')
        data = response.json()
        wc = input('В какую валюту вы хотите перевести? ')
        price = float(input('Сколько вы хотите перевести? '))
        data_rates = data["rates"]
        data_wc = float(data_rates[f'{(wc.upper())}']) * price
        return data_wc
    except Exception:
        print("Sry, bot is thinking")