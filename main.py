import requests
import os
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
SMS_API_KEY = os.environ.get("SMS_API_KEY")

SMS_SID = os.environ.get("SMS_SID")


stock_parmas = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parmas)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]


yesterday_close = data_list[0]['4. close']
day_before_close = data_list[1]['4. close']

difference = float(yesterday_close) - float(day_before_close)
diff_percent = round((difference / float(yesterday_close)) * 100)


if abs(diff_percent) >= 0:

    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()['articles']
    print(articles)
    content_list = [articles][:3]

    article_list = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in content_list]
    print(article_list)

    client = Client(SMS_SID, SMS_API_KEY)
    for article in article_list:
        message = client.messages.create(
            body=article,
            from_="+15076097388",
            to="+14703189931"
            )





