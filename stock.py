import requests

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=S35IMJ3QYC41G06N'
r = requests.get(url)
data = r.json()

print(data)