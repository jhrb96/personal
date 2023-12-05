import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import pandas as pd

# Basic Example
stock = input()





# Date range for today
end_date = dt.datetime.now()

start_date = end_date - dt.timedelta(days=365 * 5)

df = yf.download(stock, start=start_date, end=end_date)

df.head()

adj_close_prices = df['Adj Close']

log_returns = np.log(adj_close_prices/adj_close_prices.shift(1))

cumulative_log_returns = log_returns.cumsum()

cumulative_log_returns.plot(title="Cumulative Returns", figsize=(10, 6))

