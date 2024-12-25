import yfinance as yf

def get_nifty_tickers(index):
    """Return Nifty 50 or Nifty 100 tickers."""
    if index == 'nifty50':
        return [
            "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
            "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
            "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
            "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
            "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
            "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
            "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS",
            "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS",
            "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS",
            "TITAN.NS", "UPL.NS", "ULTRACEMCO.NS", "WIPRO.NS", "ZOMATO.NS"
        ]
    elif index == 'nifty100':
        return [
            "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
            "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
            "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
            "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
            "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
            "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
            "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS",
            "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS",
            "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS",
            "TITAN.NS", "UPL.NS", "ULTRACEMCO.NS", "WIPRO.NS", "ZOMATO.NS",
            "ABBOTINDIA.NS", "ACC.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "AMBUJACEM.NS",
            "AUROPHARMA.NS", "BANKBARODA.NS", "BERGEPAINT.NS", "BIOCON.NS", "BOSCHLTD.NS",
            "CADILAHC.NS", "CANBK.NS", "CHOLAFIN.NS", "COLPAL.NS", "CONCOR.NS",
            "DLF.NS", "DABUR.NS", "GAIL.NS", "GODREJCP.NS", "HAVELLS.NS",
            "HDFCAMC.NS", "HINDPETRO.NS", "ICICIGI.NS", "ICICIPRULI.NS", "INDIGO.NS",
            "IOC.NS", "JINDALSTEL.NS", "JUBLFOOD.NS", "LUPIN.NS", "MARICO.NS",
            "MCDOWELL-N.NS", "MUTHOOTFIN.NS", "NMDC.NS", "NAUKRI.NS", "PETRONET.NS",
            "PIDILITIND.NS", "PEL.NS", "PFC.NS", "PGHH.NS", "PNB.NS",
            "SBICARD.NS", "SIEMENS.NS", "TORNTPHARM.NS", "VEDL.NS", "YESBANK.NS"
        ]
    else:
        raise ValueError("Invalid index. Choose 'nifty50' or 'nifty100'.")

def fetch_nifty_data(index='nifty50', period='1y'):
    """Fetch data for Nifty 50 or Nifty 100 stocks."""
    tickers = get_nifty_tickers(index)
    return fetch_stock_data(tickers, period)
