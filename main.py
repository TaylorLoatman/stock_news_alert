import requests
import datetime as dt
import os
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


def percent_increase(t_close, former_close):
    compare_close = t_close - former_close
    percent_d = (compare_close/ t_close) * 100
    the_percent = abs(percent_d)
    return int(the_percent)


stock_api_key = os.environ.get("STOCK_API_KEY")
news_api_key = os.environ.get("NEWS_API_KEY")
sms_api_key = os.environ.get("SMS_API_KEY")

sms_sid = os.environ.get("SMS_SID")

stock_parmas = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}


resources = requests.get(url=STOCK_ENDPOINT, params=stock_parmas)
resources.raise_for_status()
data = resources.json()

now = dt.datetime.now()
today = now.date()

if today not in data['Time Series (Daily)']:
    today = now.date() - dt.timedelta(days=1)
else:
    today = now.date()


if today.weekday() == 6:
    yesterday = today - dt.timedelta(days=2)
    day_before = today - dt.timedelta(days=3)
elif today.weekday() == 0:
    yesterday = today - dt.timedelta(days=3)
    day_before = today - dt.timedelta(days=4)
else:
    yesterday = today - dt.timedelta(days=1)
    day_before = today - dt.timedelta(days=2)


today_close = data['Time Series (Daily)'][f'{today}']['4. close']
yesterday_close = data['Time Series (Daily)'][f'{yesterday}']['4. close']
day_before_close = data['Time Series (Daily)'][f'{day_before}']['4. close']

close_days = [float(today_close), float(yesterday_close), float(day_before_close)]

first_compare = percent_increase(close_days[0], close_days[1])
second_compare = percent_increase(close_days[0], close_days[2])

if first_compare >= 5 and second_compare >= 5:
    pass

    news_params = {
        "q": COMPANY_NAME,
        "from": today,
        "sortBy": 'publishedAt',
        "apiKey": news_api_key
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()

    content_list = news_data['articles'][:3]
    article_list = [[content_list[0]['title'], content_list[0]['description']], [content_list[1]['title'],
                    content_list[1]['description']], [content_list[2]['title'], content_list[2]['description']]]

    client = Client(sms_sid, sms_api_key)
    message = client.messages.create(
        body= f"{STOCK_NAME}\n\nHeadline: {article_list[0][0]}\n\nBrief: {article_list[0][1]}",
        from_="+15076097388",
        to="+14703189931"
        )
    print(message.status)




