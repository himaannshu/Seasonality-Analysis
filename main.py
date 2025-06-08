import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Commodity/Energy Stock Seasonality Analysis & Backtest")

# --- Sidebar: Commodity Ticker Selection ---
st.sidebar.header("Commodity/Energy Symbols")
commodity_symbols = {
    "Crude Oil": "CL=F",
    "Natural Gas": "NG=F",
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Copper": "HG=F",
    "Corn": "ZC=F",
    "Wheat": "ZW=F",
    "Soybeans": "ZS=F",
    "Heating Oil": "HO=F",
    "Gasoline": "RB=F",
    "Brent Crude": "BZ=F"
}
selected_name = st.sidebar.selectbox("Select Commodity", list(commodity_symbols.keys()))
ticker = commodity_symbols[selected_name]

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2010-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

if start_date >= end_date:
    st.error("Start Date must be before End Date")
    st.stop()

run_analysis = st.button("Run Analysis")

if run_analysis:

    @st.cache_data(ttl=3600)
    def load_data(ticker, start, end):
        df = yf.download(ticker, start=start, end=end)
        df.reset_index(inplace=True)
        df.insert(0, "Price", ticker)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Return'] = df['Close'].pct_change()
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['Month_Name'] = df['Date'].dt.strftime('%b')
        df.set_index('Date', inplace=True)
        return df

    df = load_data(ticker, start_date, end_date)
    if df.empty:
        st.error("No data found for this ticker or date range.")
        st.stop()

    st.header("Seasonality Analysis")

    monthly_returns = df.groupby(['Year', 'Month'])['Return'].sum().unstack()
    avg_monthly_returns = monthly_returns.mean(axis=0)

    fig, ax = plt.subplots(1, 2, figsize=(14, 5))

    # Heatmap
    sns.heatmap(monthly_returns, cmap='RdYlGn', center=0, ax=ax[0], cbar_kws={'label': 'Monthly Return'})
    ax[0].set_title('Monthly Returns Heatmap (by Year)')
    ax[0].set_ylabel('Year')
    ax[0].set_xlabel('Month')
    ax[0].set_xticks(np.arange(12) + 0.5)
    ax[0].set_xticklabels([pd.Timestamp(month=i, day=1, year=2000).strftime('%b') for i in range(1, 13)])

    # Bar plot
    avg_monthly_returns.index = [pd.Timestamp(month=i, day=1, year=2000).strftime('%b') for i in avg_monthly_returns.index]
    avg_monthly_returns.plot(kind='bar', color='skyblue', ax=ax[1])
    ax[1].set_title('Average Monthly Returns')
    ax[1].set_ylabel('Average Return')
    ax[1].set_xlabel('Month')

    st.pyplot(fig)

    st.header("Trading Signals Based on Monthly Seasonality")

    best_months = avg_monthly_returns.sort_values(ascending=False).head(3).index.to_list()
    st.write(f"Best months to be LONG based on average returns: {best_months}")

    df['Signal'] = np.where(df['Month_Name'].isin(best_months), 1, 0)
    st.write(df['Signal'].value_counts().rename({0: 'Sell/No Position', 1: 'Buy'}))

    # Backtesting
    st.header("Backtest Results")

    df['Strategy_Return'] = df['Return'] * df['Signal'].shift(1)
    df['Cumulative_Market_Return'] = (1 + df['Return']).cumprod() - 1
    df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod() - 1

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    df['Cumulative_Market_Return'].plot(ax=ax2, label='Buy & Hold Market Return', color='gray')
    df['Cumulative_Strategy_Return'].plot(ax=ax2, label='Seasonality Strategy Return', color='green')
    ax2.set_ylabel("Cumulative Return")
    ax2.set_title("Backtest Equity Curve")
    ax2.legend()
    st.pyplot(fig2)

    total_return = df['Cumulative_Strategy_Return'].iloc[-1]
    market_return = df['Cumulative_Market_Return'].iloc[-1]
    sharpe_ratio = df['Strategy_Return'].mean() / df['Strategy_Return'].std() * np.sqrt(252) if df['Strategy_Return'].std() != 0 else np.nan

    st.markdown(f"""
    **Strategy Total Return:** {total_return:.2%}  
    **Buy & Hold Market Return:** {market_return:.2%}  
    **Strategy Sharpe Ratio (Annualized):** {sharpe_ratio:.2f}  
    """)

    st.success("Seasonality analysis and backtesting complete!")
