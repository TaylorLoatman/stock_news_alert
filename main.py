import requests
import datetime as dt


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
FIVE_PERCENT = 5

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


def percent_increase(today_close, former_close):
    compare_close = today_close - former_close
    percent_d = (compare_close/ today_close) * 100
    the_percent = abs(percent_d)
    print(int(the_percent))


stock_api_key = "YE5EUWQ9MOHC73CL"

stock_parmas = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

resources = requests.get(url=STOCK_ENDPOINT, params=stock_parmas)
resources.raise_for_status()
data = resources.json()

now = dt.datetime.now()
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


today_close = float(data['Time Series (Daily)'][f'{today}']['4. close'])
yesterday_close = float(data['Time Series (Daily)'][f'{yesterday}']['4. close'])
day_before_close = float(data['Time Series (Daily)'][f'{day_before}']['4. close'])

# print(today_close)
# print(yesterday_close)
print(day_before_close)
percent_increase(today_close, day_before_close)


