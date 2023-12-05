import yfinance as yf
import fredapi as fd
import datetime as dt
import tabulate

# US Treasury Interest Rate (10 Year) https://finance.yahoo.com/quote/%5ETNX/
tbill = yf.Ticker("^TNX")
t_bill_todayData = tbill.history(period='1d')
t_bill_rate = t_bill_todayData['Close'][0]/100

# Median CPI from Federal Reserve of St Louis https://fred.stlouisfed.org/series/MEDCPIM158SFRBCLE
fred = fd.Fred(api_key='84b9e6cdaee1e176e6adc7079fb339a0')
CPI_Data = fred.get_series_latest_release('MEDCPIM158SFRBCLE')
CPI = CPI_Data[-1]/100

# SPDR S&P 500 ETF Trust (SPY) https://finance.yahoo.com/quote/SPY?p=SPY&.tsrc=fin-srch
end_date = dt.datetime.now() - dt.timedelta(days=365 * 10)
start_date = end_date - dt.timedelta(days=2)

SPY = yf.Ticker("SPY")
SPY_todayData = SPY.history(period='1d')
SPY_Price = SPY_todayData['Close'][0]

SPY_10Y = SPY.history(start=start_date, end=end_date, period='1d')
SPY_Price_10Y = SPY_10Y['Close'][-1]

SPY_Average_Return = pow((SPY_Price/SPY_Price_10Y), 1/10) - 1