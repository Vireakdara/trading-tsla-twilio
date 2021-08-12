import requests
import datetime as dt
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = "AC1a2e3805a4c6aee7de25f314bdf8db03"
auth_token = "04ffcb32152e022686ba56a98c3f2f0b"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "YLV7PEVRKPMCBNV0"
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data_stock = response.json()["Time Series (Daily)"]

data_stock_list = [value for (key, value) in data_stock.items()]
yesterday_stock = data_stock_list[0]["4. close"]

day_before_yesterday_stock = data_stock_list[1]["4. close"]
positive_difference = float(yesterday_stock) - float(day_before_yesterday_stock)
emoji = None
if positive_difference > 0:
    emoji = "🔺"
else:
    emoji = "🔻"

difference_percents = (positive_difference / float(yesterday_stock)) * 100
print(difference_percents)

if difference_percents > -1:
    print("Get News")
    news_params = {
        "q": COMPANY_NAME,
        "language": "en",
        "pageSize": 1,
        "apiKey": "40d5c684809e4d889c53efe47e1f8426"

    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    data_news = news_response.json()["articles"]
    # Angela's method
    formatted_news = [f"Headline: {news_article['title']}. \nBrief: {news_article['description']}" for news_article in
                      data_news]
    print(formatted_news)

    for article in formatted_news:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"TSLA {emoji}{positive_difference}{article}",
            from_="+18507249985",
            to="+85510231957"
        )
        print(message.status)


    # Dara's method
    # data_news_title_list = []
    # data_news_description_list = []
    # for arr in range(0, 3):
    #     data_news_title = data_news[arr]["title"]
    #     data_news_title_list.append(data_news_title)
    #
    #     data_news_description = data_news[arr]["description"]
    #     data_news_description_list.append(data_news_description)
    #
    # print(data_news_title_list)
    # print(data_news_description_list)
    #
    # client = Client(account_sid, auth_token)
    # message = client.messages \
    #     .create(
    #     body=f"TSLA: 🔺2% "
    #          f"Headline:{data_news_title_list[0]}"
    #          f"Brief:{data_news_description_list[0]}",
    #     from_="+18507249985",
    #     to="+85510231957"
    # )
    # print(message.status)

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
