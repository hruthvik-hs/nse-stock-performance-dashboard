# 📈 NSE Stock Performance Dashboard

**Author:** Hruthvik HS  
**Tools:** Python · Pandas · NumPy · Matplotlib · yfinance  
**Domain:** Data Analytics · Financial Markets · Equity Research

---

## 📌 Project Overview

This project performs an end-to-end analysis of 5 blue-chip NSE-listed Indian stocks over a 3-year period (Jan 2022 – Dec 2024). It generates a comprehensive, multi-panel performance dashboard covering price trends, returns, volatility, correlation, and key risk-adjusted metrics.

**Stocks Analysed:**
| Ticker | Company |
|--------|---------|
| RELIANCE | Reliance Industries Ltd |
| TCS | Tata Consultancy Services |
| INFY | Infosys Ltd |
| HDFCBANK | HDFC Bank Ltd |
| WIPRO | Wipro Ltd |

---

## 📊 Dashboard Panels

| Panel | Description |
|-------|-------------|
| Cumulative Returns | 3-year compounded return trajectory for all 5 stocks |
| Price & Moving Averages | TCS price with MA20, MA50, MA200 overlays |
| Rolling Volatility | 30-day annualised volatility across all stocks |
| Total Return Bar Chart | Side-by-side total return comparison |
| Correlation Heatmap | Daily return correlation matrix across all stocks |
| KPI Summary Table | Start/end price, total return, Sharpe ratio, max drawdown, volatility |

---

## 📐 Metrics Calculated

- **Total Return %** — Price appreciation over the full period
- **Sharpe Ratio** — Risk-adjusted return (6.5% Indian risk-free rate baseline)
- **Maximum Drawdown** — Largest peak-to-trough decline
- **Annualised Volatility** — Standard deviation of daily returns × √252
- **Rolling Volatility** — 30-day window annualised volatility
- **Moving Averages** — 20-day, 50-day, 200-day SMAs
- **Return Correlation** — Cross-stock daily return correlation matrix

---

## 🚀 How to Run (Live Data Version)

```bash
# Install dependencies
pip install yfinance pandas numpy matplotlib

# Run live version
python live_version.py
```

This fetches real-time data from Yahoo Finance for the NSE tickers.

---

## 📁 Project Structure

```
Project1_Stock_Dashboard/
│
├── analysis.py          # Main analysis script (simulation data)
├── live_version.py      # Live data version using yfinance
├── stock_dashboard.png  # Generated dashboard image
├── nse_stock_data.csv   # Raw OHLCV stock data (782 trading days × 5 stocks)
├── summary_metrics.csv  # KPI summary table
└── README.md            # This file
```

---

## 💡 Key Findings

- **INFY** delivered the strongest risk-adjusted returns over the period
- **HDFCBANK** showed the lowest volatility — most stable among the five
- High correlation (>0.70) observed between IT stocks (TCS, INFY, WIPRO) — suggesting sector-level co-movement
- **RELIANCE** acted as a partial diversifier with lower correlation to IT peers
- All stocks experienced elevated volatility in mid-2022 aligned with global macro events (Fed rate hikes, FII outflows)

---

## 🛠️ Skills Demonstrated

- Financial data acquisition and preprocessing
- Time-series analysis and feature engineering
- Risk metric computation (Sharpe, drawdown, volatility)
- Multi-panel data visualisation with Matplotlib
- Equity market domain knowledge (NSE, moving averages, correlation analysis)

---

*This project was built as part of a personal analytics portfolio to demonstrate applied data science skills in the financial domain.*
