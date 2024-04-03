import requests
from twilio.rest import Client
import os

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"
stock_api_key = os.getenv("stock_api_key")
news_api_key = os.getenv("news_api_key")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
    "outputsize": "compact",
    "datatype": "json"
}

news_params = {
    "qInTitle": COMPANY_NAME,
    "apiKey": news_api_key
}

stock_response = requests.get(STOCK_URL, params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
print(stock_data)
stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_closing_price = stock_data_list[0]["4. close"]
day_before_yesterday = stock_data_list[1]["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday)
up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

diff_percent = round((difference / float(yesterday_closing_price)) * 100, 2)
print(f"{diff_percent}%")

news_response = requests.get(NEWS_URL, params=news_params)
news_response.raise_for_status()
news = news_response.json()

if abs(diff_percent) > 0:
    articles = news["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}. \nLink: {article['url']}"
                          for article in three_articles]

    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            from_='+12569739894',
            to='+254716517329',
            body=article
        )
        print(message.status)
# print(news_response.json())
