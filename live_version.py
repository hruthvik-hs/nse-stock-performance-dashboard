"""
LIVE VERSION — Run this on your local machine
Requirements: pip install yfinance pandas matplotlib seaborn

This script fetches real NSE stock data from Yahoo Finance
and generates the same dashboard with live data.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── Config ────────────────────────────────────────────────────────────────────
TICKERS = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS':      'TCS.NS',
    'INFY':     'INFY.NS',
    'HDFCBANK': 'HDFCBANK.NS',
    'WIPRO':    'WIPRO.NS',
}
START = '2022-01-01'
END   = '2024-12-31'

COLORS = {
    'RELIANCE': '#E63946',
    'TCS':      '#2196F3',
    'INFY':     '#4CAF50',
    'HDFCBANK': '#FF9800',
    'WIPRO':    '#9C27B0',
}

# ── Fetch Data ────────────────────────────────────────────────────────────────
print("Fetching live data from Yahoo Finance...")
raw = yf.download(list(TICKERS.values()), start=START, end=END)['Close']
raw.columns = list(TICKERS.keys())
pivot = raw.dropna()

print(f"✅ Fetched {len(pivot)} trading days")
print(f"   Range: {pivot.index[0].date()} to {pivot.index[-1].date()}")

# ── Metrics ───────────────────────────────────────────────────────────────────
returns      = pivot.pct_change().dropna()
cum_returns  = (1 + returns).cumprod() - 1
volatility   = returns.rolling(30).std() * np.sqrt(252) * 100
total_return = ((pivot.iloc[-1] - pivot.iloc[0]) / pivot.iloc[0] * 100).round(2)
rf           = 0.065 / 252
sharpe       = ((returns.mean() - rf) / returns.std() * np.sqrt(252)).round(2)

def max_drawdown(series):
    roll_max = series.cummax()
    return round(((series - roll_max) / roll_max).min() * 100, 2)

drawdowns = {t: max_drawdown(pivot[t]) for t in TICKERS}

# Moving averages for TCS
ma_data = {}
for ticker in TICKERS:
    s = pivot[ticker]
    ma_data[ticker] = {
        'price': s, 'MA20': s.rolling(20).mean(),
        'MA50': s.rolling(50).mean(), 'MA200': s.rolling(200).mean(),
    }

# ── Dashboard (same layout as simulation version) ────────────────────────────
BG = '#0D1117'; PANEL = '#161B22'; TEXT = '#E6EDF3'
SUBTEXT = '#8B949E'; ACCENT = '#1F6FEB'; GREEN = '#3FB950'; RED = '#F85149'

fig = plt.figure(figsize=(20, 24), facecolor=BG)
gs  = gridspec.GridSpec(4, 2, figure=fig, hspace=0.45, wspace=0.3,
                        top=0.93, bottom=0.04, left=0.06, right=0.97)

fig.text(0.5, 0.965, 'NSE STOCK PERFORMANCE DASHBOARD', ha='center',
         fontsize=22, fontweight='bold', color=TEXT, fontfamily='monospace')
fig.text(0.5, 0.950,
         f'Indian Equity Market Analysis  |  {START} to {END}  |  5 Blue-Chip NSE Stocks',
         ha='center', fontsize=11, color=SUBTEXT)

# Chart 1: Cumulative Returns
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor(PANEL)
for t in TICKERS:
    ax1.plot(cum_returns.index, cum_returns[t]*100, color=COLORS[t], linewidth=1.8, label=t)
ax1.axhline(0, color=SUBTEXT, linewidth=0.8, linestyle='--', alpha=0.5)
ax1.set_title('Cumulative Returns (%)', color=TEXT, fontsize=13, fontweight='bold', pad=10)
ax1.tick_params(colors=SUBTEXT); ax1.legend(facecolor=PANEL, edgecolor='#30363D', labelcolor=TEXT, ncol=5)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
for spine in ax1.spines.values(): spine.set_color('#30363D')
ax1.grid(axis='y', alpha=0.15, color=SUBTEXT)

# Charts 2-6: same structure as simulation version
# (copy remaining charts from analysis.py)

plt.savefig('stock_dashboard_LIVE.png', dpi=150, bbox_inches='tight', facecolor=BG)
print("✅ Live dashboard saved as stock_dashboard_LIVE.png")

# Save data
pivot.reset_index().to_csv('nse_stock_data_live.csv', index=False)
print("✅ Live data CSV saved!")
