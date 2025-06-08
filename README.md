
# 📈 Commodity Seasonality Analysis & Strategy Backtest

This Streamlit app allows you to **analyze historical seasonality** in commodities (like Crude Oil, Natural Gas, etc.) and **backtest a simple trading strategy** based on seasonal patterns.

> 🔁 _"History doesn’t repeat itself, but it often rhymes."_ — Mark Twain  
> This app helps you find those rhymes in the financial markets.

---

## 🚀 Features

- 🔍 **Seasonality Analysis**  
  Visualize **monthly returns** over time using heatmaps and bar charts.

- 🧠 **Best-Month Strategy**  
  Identify the **top 3 most profitable months** on average and generate simple **buy/sell signals** accordingly.

- 📊 **Backtest Dashboard**  
  Compare the cumulative returns of:
  - 🟢 Seasonality-based strategy
  - ⚫️ Buy & Hold approach

- 💬 Interactive Streamlit UI with user input for:
  - Ticker (e.g. `CL=F`, `NG=F`)
  - Date Range
  - Sidebar list of commodity tickers
  - “Run Analysis” button to start

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/commodity-seasonality-analysis.git
cd commodity-seasonality-analysis
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧠 How the Strategy Works

1. **Fetch historical data** using [Yahoo Finance](https://finance.yahoo.com).
2. **Calculate monthly returns** for each year.
3. **Rank average monthly returns** across years.
4. **Identify top 3 months** — these become “Buy” months.
5. **Simulate a strategy** that:
   - Enters long positions during these months
   - Exits otherwise
6. **Compare** to Buy & Hold using cumulative return charts and Sharpe ratio.

---

## 📌 Sample Tickers

| Commodity | Ticker |
|----------|--------|
| Crude Oil (WTI) | `CL=F` |
| Natural Gas | `NG=F` |
| Heating Oil | `HO=F` |
| Gold | `GC=F` |
| Silver | `SI=F` |
| Corn | `ZC=F` |
| Soybeans | `ZS=F` |
| Wheat | `ZW=F` |

---

## 📷 Screenshots

![Heatmap](screenshots/heatmap.png)
![Backtest](screenshots/backtest.png)

---

## 📈 Example Insights

- Crude oil tends to **perform better during summer months**.
- Natural gas often sees **strong seasonality in winter**.
- Simple seasonal timing can **outperform naive Buy & Hold**.

---

## 🙌 Acknowledgements

- Built with **Python**, **Pandas**, **Matplotlib**, **Seaborn**, **Streamlit**
- Data via **yfinance**

---

## 📬 Connect

If you found this useful, feel free to ⭐️ the repo, open an issue, or connect with me on [LinkedIn](https://www.linkedin.com/in/ayushgoel02/).

---

## 📃 License

This project is licensed under the MIT License.
