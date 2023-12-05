import yfinance as yf
import fredapi as fd

# US Treasury Yield (30 Year) https://finance.yahoo.com/quote/%5ETYX/
tickerData = yf.Ticker("^TYX")
todayData = tickerData.history(period='1d')
nominal_rate = todayData['Close'][0]/100

print("Treasury yield is", nominal_rate)

# Median CPI from Federal Reserve of St Louis https://fred.stlouisfed.org/series/MEDCPIM158SFRBCLE
fred = fd.Fred(api_key='84b9e6cdaee1e176e6adc7079fb339a0')
CPI_Data = fred.get_series_latest_release('MEDCPIM158SFRBCLE')
inflation_rate = CPI_Data[-1]/100

print("Inflation is", inflation_rate)

risk_free_return_rate = ((1+nominal_rate)/(1+inflation_rate))-1

print("The risk free rate of return is", risk_free_return_rate)
