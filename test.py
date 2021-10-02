import csv
import datetime
import dateutil
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def getFileData(fileName):
    file = fileName
    now = datetime.now()
    previous_year = now+relativedelta(years=-1)
    date_final = previous_year.strftime("%#m/%#d/%Y %#H:%M")
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        line_count = 0
        for row in reader:
            if date_final == row[1]:
                historical_price = float(row[3])
                line_count += 1
                break
            else:
                continue
        return historical_price

def getCurrentPrice(ticker, historicalData, amount):
    url = 'https://api.cryptowat.ch/markets/kraken/' + ticker + '/price'
    headers = {
      'Accepts': 'application/json'
    }
    session = Session()
    session.headers.update(headers)
    try:
      response = session.get(url)
      data = json.loads(response.text)
      current_price =data['result']['price']
      current_thousand = amount / current_price
      price_diff = current_price - historicalData
      thousand_diff =  ((amount/historicalData) - current_thousand) * current_price
      print(f'Current price {ticker}: {current_price} | Historical price {ticker}: {historicalData} | Price differnce {price_diff} | Outcome {thousand_diff}')
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

data = getFileData('gemini_ETHUSD_2020_1min.csv')
data2 = getFileData('gemini_BTCUSD_2020_1min.csv')
data3 = getFileData('gemini_LTCUSD_2020_1min.csv')
getCurrentPrice('ethusd', data, 1000)
getCurrentPrice('btcusd', data2, 1000)
getCurrentPrice('ltcusd', data3, 1000)
