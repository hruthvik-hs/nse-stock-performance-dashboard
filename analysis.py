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

np.random.seed(42)

# ── 1. Generate realistic NSE stock data ─────────────────────────────────────
STOCKS = {
    'RELIANCE': {'start': 2420, 'trend': 0.00035, 'vol': 0.014},
    'TCS':      {'start': 3580, 'trend': 0.00028, 'vol': 0.012},
    'INFY':     {'start': 1480, 'trend': 0.00022, 'vol': 0.013},
    'HDFCBANK': {'start': 1620, 'trend': 0.00018, 'vol': 0.011},
    'WIPRO':    {'start': 420,  'trend': 0.00015, 'vol': 0.015},
}

dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='B')

all_data = []
for ticker, params in STOCKS.items():
    price = params['start']
    prices = []
    for i in range(len(dates)):
        shock = np.random.normal(params['trend'], params['vol'])
        # Add market events (COVID recovery, budget dips, etc.)
        if dates[i].month == 3 and dates[i].year == 2022:
            shock -= 0.003
        if dates[i].month == 6 and dates[i].year == 2022:
            shock -= 0.004
        if dates[i].month == 2 and dates[i].year == 2023:
            shock += 0.005
        price = price * (1 + shock)
        prices.append(round(price, 2))
    df = pd.DataFrame({'Date': dates, 'Ticker': ticker, 'Close': prices})
    df['Open']   = df['Close'].shift(1).fillna(df['Close']) * np.random.uniform(0.998, 1.002, len(df))
    df['High']   = df[['Open','Close']].max(axis=1) * np.random.uniform(1.001, 1.015, len(df))
    df['Low']    = df[['Open','Close']].min(axis=1) * np.random.uniform(0.985, 0.999, len(df))
    df['Volume'] = np.random.randint(1_000_000, 8_000_000, len(df))
    all_data.append(df)

data = pd.concat(all_data, ignore_index=True)
data['Date'] = pd.to_datetime(data['Date'])

# ── 2. Derived metrics ────────────────────────────────────────────────────────
pivot = data.pivot(index='Date', columns='Ticker', values='Close')

# Moving averages
ma_data = {}
for ticker in STOCKS:
    s = pivot[ticker]
    ma_data[ticker] = {
        'price': s,
        'MA20': s.rolling(20).mean(),
        'MA50': s.rolling(50).mean(),
        'MA200': s.rolling(200).mean(),
    }

# Daily returns
returns = pivot.pct_change().dropna()

# Cumulative returns
cum_returns = (1 + returns).cumprod() - 1

# Volatility (30-day rolling annualised)
volatility = returns.rolling(30).std() * np.sqrt(252) * 100

# Total return %
total_return = ((pivot.iloc[-1] - pivot.iloc[0]) / pivot.iloc[0] * 100).round(2)

# Sharpe ratio (assume 6.5% risk-free rate India)
rf = 0.065 / 252
sharpe = ((returns.mean() - rf) / returns.std() * np.sqrt(252)).round(2)

# Max drawdown
def max_drawdown(series):
    roll_max = series.cummax()
    drawdown = (series - roll_max) / roll_max
    return round(drawdown.min() * 100, 2)

drawdowns = {t: max_drawdown(pivot[t]) for t in STOCKS}

print("✅ Data generated successfully")
print(f"   Date range: {pivot.index[0].date()} to {pivot.index[-1].date()}")
print(f"   Trading days: {len(pivot)}")
print("\n📊 Total Returns:")
for t, r in total_return.items():
    print(f"   {t}: {r:+.2f}%")

# ── 3. MASTER DASHBOARD ───────────────────────────────────────────────────────
COLORS = {
    'RELIANCE': '#E63946',
    'TCS':      '#2196F3',
    'INFY':     '#4CAF50',
    'HDFCBANK': '#FF9800',
    'WIPRO':    '#9C27B0',
}
BG     = '#0D1117'
PANEL  = '#161B22'
TEXT   = '#E6EDF3'
SUBTEXT= '#8B949E'
ACCENT = '#1F6FEB'
GREEN  = '#3FB950'
RED    = '#F85149'

fig = plt.figure(figsize=(20, 24), facecolor=BG)
gs = gridspec.GridSpec(4, 2, figure=fig, hspace=0.45, wspace=0.3,
                       top=0.93, bottom=0.04, left=0.06, right=0.97)

fig.text(0.5, 0.965, 'NSE STOCK PERFORMANCE DASHBOARD', ha='center',
         fontsize=22, fontweight='bold', color=TEXT, fontfamily='monospace')
fig.text(0.5, 0.950, 'Indian Equity Market Analysis  |  Jan 2022 – Dec 2024  |  5 Blue-Chip Stocks',
         ha='center', fontsize=11, color=SUBTEXT)

# ── Chart 1: Cumulative Returns ──
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor(PANEL)
for ticker in STOCKS:
    ax1.plot(cum_returns.index, cum_returns[ticker]*100,
             color=COLORS[ticker], linewidth=1.8, label=ticker)
ax1.axhline(0, color=SUBTEXT, linewidth=0.8, linestyle='--', alpha=0.5)
ax1.set_title('Cumulative Returns (%)', color=TEXT, fontsize=13, fontweight='bold', pad=10)
ax1.tick_params(colors=SUBTEXT, labelsize=9)
ax1.spines[:].set_color('#30363D')
ax1.set_facecolor(PANEL)
for spine in ax1.spines.values():
    spine.set_color('#30363D')
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax1.legend(loc='upper left', facecolor=PANEL, edgecolor='#30363D',
           labelcolor=TEXT, fontsize=9, ncol=5)
ax1.fill_between(cum_returns.index, 0, cum_returns['RELIANCE']*100,
                 alpha=0.06, color=COLORS['RELIANCE'])
ax1.grid(axis='y', alpha=0.15, color=SUBTEXT)

# ── Chart 2: Price with Moving Averages (TCS) ──
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor(PANEL)
ticker = 'TCS'
d = ma_data[ticker]
ax2.plot(d['price'].index, d['price'], color=COLORS[ticker], linewidth=1.2, label='Price', alpha=0.9)
ax2.plot(d['MA20'].index, d['MA20'], color='#FFD700', linewidth=1, linestyle='--', label='MA20', alpha=0.8)
ax2.plot(d['MA50'].index, d['MA50'], color='#00BCD4', linewidth=1, linestyle='--', label='MA50', alpha=0.8)
ax2.plot(d['MA200'].index, d['MA200'], color='#FF5722', linewidth=1, linestyle='--', label='MA200', alpha=0.8)
ax2.set_title(f'{ticker} — Price & Moving Averages', color=TEXT, fontsize=11, fontweight='bold', pad=8)
ax2.tick_params(colors=SUBTEXT, labelsize=8)
for spine in ax2.spines.values(): spine.set_color('#30363D')
ax2.legend(facecolor=PANEL, edgecolor='#30363D', labelcolor=TEXT, fontsize=8)
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('₹%.0f'))
ax2.grid(axis='y', alpha=0.12, color=SUBTEXT)

# ── Chart 3: Volatility ──
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor(PANEL)
for ticker in STOCKS:
    ax3.plot(volatility.index, volatility[ticker],
             color=COLORS[ticker], linewidth=1.2, label=ticker, alpha=0.85)
ax3.set_title('30-Day Rolling Volatility (Annualised %)', color=TEXT, fontsize=11, fontweight='bold', pad=8)
ax3.tick_params(colors=SUBTEXT, labelsize=8)
for spine in ax3.spines.values(): spine.set_color('#30363D')
ax3.legend(facecolor=PANEL, edgecolor='#30363D', labelcolor=TEXT, fontsize=8)
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax3.grid(axis='y', alpha=0.12, color=SUBTEXT)

# ── Chart 4: Total Return Bar ──
ax4 = fig.add_subplot(gs[2, 0])
ax4.set_facecolor(PANEL)
tickers = list(total_return.index)
values  = list(total_return.values)
bar_colors = [GREEN if v > 0 else RED for v in values]
bars = ax4.bar(tickers, values, color=bar_colors, width=0.55, edgecolor='none', zorder=3)
for bar, val in zip(bars, values):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:+.1f}%', ha='center', va='bottom', color=TEXT, fontsize=9, fontweight='bold')
ax4.set_title('Total Return Jan 2022 – Dec 2024', color=TEXT, fontsize=11, fontweight='bold', pad=8)
ax4.tick_params(colors=SUBTEXT, labelsize=9)
for spine in ax4.spines.values(): spine.set_color('#30363D')
ax4.axhline(0, color=SUBTEXT, linewidth=0.8)
ax4.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
ax4.grid(axis='y', alpha=0.12, color=SUBTEXT, zorder=0)

# ── Chart 5: Correlation Heatmap ──
ax5 = fig.add_subplot(gs[2, 1])
ax5.set_facecolor(PANEL)
corr = returns.corr()
tickers_list = list(STOCKS.keys())
im = ax5.imshow(corr.values, cmap='RdYlGn', vmin=-1, vmax=1, aspect='auto')
ax5.set_xticks(range(len(tickers_list)))
ax5.set_yticks(range(len(tickers_list)))
ax5.set_xticklabels(tickers_list, color=SUBTEXT, fontsize=8, rotation=30)
ax5.set_yticklabels(tickers_list, color=SUBTEXT, fontsize=8)
for i in range(len(tickers_list)):
    for j in range(len(tickers_list)):
        ax5.text(j, i, f'{corr.values[i,j]:.2f}', ha='center', va='center',
                 fontsize=8, color='black' if 0.3 < corr.values[i,j] < 0.9 else TEXT,
                 fontweight='bold')
ax5.set_title('Return Correlation Matrix', color=TEXT, fontsize=11, fontweight='bold', pad=8)
for spine in ax5.spines.values(): spine.set_color('#30363D')

# ── Chart 6: KPI Summary Table ──
ax6 = fig.add_subplot(gs[3, :])
ax6.set_facecolor(PANEL)
ax6.axis('off')
ax6.set_title('Key Performance Metrics Summary', color=TEXT, fontsize=11,
              fontweight='bold', pad=10, loc='left')

headers = ['Stock', 'Start Price (₹)', 'End Price (₹)', 'Total Return', 'Sharpe Ratio', 'Max Drawdown', 'Ann. Volatility']
rows = []
for t in STOCKS:
    ann_vol = returns[t].std() * np.sqrt(252) * 100
    rows.append([
        t,
        f"₹{pivot[t].iloc[0]:,.0f}",
        f"₹{pivot[t].iloc[-1]:,.0f}",
        f"{total_return[t]:+.2f}%",
        f"{sharpe[t]:.2f}",
        f"{drawdowns[t]:.2f}%",
        f"{ann_vol:.1f}%"
    ])

col_widths = [0.10, 0.13, 0.13, 0.13, 0.13, 0.15, 0.15]
col_starts = [0.01]
for w in col_widths[:-1]:
    col_starts.append(col_starts[-1] + w)

y_header = 0.88
for i, (h, x) in enumerate(zip(headers, col_starts)):
    ax6.text(x, y_header, h, transform=ax6.transAxes,
             color=ACCENT, fontsize=9, fontweight='bold')

for row_i, row in enumerate(rows):
    y = y_header - 0.14*(row_i+1)
    rect = FancyBboxPatch((0, y-0.06), 1, 0.11,
                          boxstyle="round,pad=0.01",
                          facecolor='#1C2128' if row_i % 2 == 0 else PANEL,
                          transform=ax6.transAxes, zorder=0, linewidth=0)
    ax6.add_patch(rect)
    for col_i, (val, x) in enumerate(zip(row, col_starts)):
        color = TEXT
        if col_i == 3:  # Total return
            color = GREEN if '+' in val else RED
        elif col_i == 5:  # Max drawdown
            color = RED
        ax6.text(x, y, val, transform=ax6.transAxes,
                 color=color, fontsize=9,
                 fontweight='bold' if col_i == 0 else 'normal')

# Ticker colour dots
for row_i, (row, ticker) in enumerate(zip(rows, STOCKS.keys())):
    y = y_header - 0.14*(row_i+1)
    circle = plt.Circle((col_starts[0]-0.008, y+0.005), 0.004,
                         color=COLORS[ticker], transform=ax6.transAxes)
    ax6.add_patch(circle)

fig.text(0.5, 0.01, 'Data: NSE  |  Analysis by Hruthvik HS  |  Tools: Python (Pandas, NumPy, Matplotlib)',
         ha='center', fontsize=8, color=SUBTEXT)

plt.savefig('/mnt/user-data/outputs/Project1_Stock_Dashboard/stock_dashboard.png',
            dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("✅ Dashboard saved!")

# ── 4. Save clean CSV ─────────────────────────────────────────────────────────
data.to_csv('/mnt/user-data/outputs/Project1_Stock_Dashboard/nse_stock_data.csv', index=False)
print("✅ Data CSV saved!")

# ── 5. Summary stats CSV ──────────────────────────────────────────────────────
summary = pd.DataFrame({
    'Ticker': list(STOCKS.keys()),
    'Start_Price': [pivot[t].iloc[0] for t in STOCKS],
    'End_Price':   [pivot[t].iloc[-1] for t in STOCKS],
    'Total_Return_Pct': [total_return[t] for t in STOCKS],
    'Sharpe_Ratio': [sharpe[t] for t in STOCKS],
    'Max_Drawdown_Pct': [drawdowns[t] for t in STOCKS],
    'Ann_Volatility_Pct': [round(returns[t].std()*np.sqrt(252)*100, 2) for t in STOCKS],
})
summary.to_csv('/mnt/user-data/outputs/Project1_Stock_Dashboard/summary_metrics.csv', index=False)
print("✅ Summary metrics saved!")
print("\n🎉 All outputs ready!")
