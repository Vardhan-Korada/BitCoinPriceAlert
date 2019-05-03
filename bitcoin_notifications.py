import requests
import time
from datetime import datetime
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/nCIde9Yn2TbodY9RlIi_7YWY0IWwpDh4i50EPaUCqGv'
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
BITCOIN_PRICE_THRESHOLD = 10000

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event,value):
    data = {'value1':value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    print(ifttt_event_url)
    requests.post(ifttt_event_url, json=data)


def main():
    bitcoin_history = []
    while True:
        print("I'm here..")
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            bitcoin_history = []
        time.sleep(1 * 60)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)


if __name__ == "__main__":
    main()
