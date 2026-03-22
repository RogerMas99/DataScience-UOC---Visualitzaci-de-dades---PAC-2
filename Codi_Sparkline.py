import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# ── Data ──────────────────────────────────────────────────────────────────────
tickers = ['ITX.MC', 'SAN.MC', 'IBE.MC', 'BBVA.MC', 'CABK.MC',
           'MT.AS', 'FER.MC', 'AENA.MC', 'ELE.MC', 'REP.MC']

noms = ['Inditex', 'Banco Santander', 'Iberdrola', 'BBVA', 'CaixaBank',
        'ArcelorMittal', 'Ferrovial', 'Aena', 'Endesa', 'Repsol']

sectors = ['Consum Discrecional', 'Financer', 'Energia / Utilities', 'Financer', 'Financer',
           'Materials Bàsics', 'Infraestructures', 'Infraestructures', 'Energia / Utilities', 'Energia']

dades = yf.download(tickers, period="3mo", progress=False)['Close']

# ── Palette & style ───────────────────────────────────────────────────────────
BG        = '#0D0F14'
CARD      = '#13161E'
BORDER    = '#1E2330'
TEXT_PRI  = '#F0F2F7'
TEXT_SEC  = '#6B7494'
ACCENT    = '#C8A96E'       # gold
GREEN     = '#3ECFA4'
RED       = '#F26E6E'
GRID_COL  = '#1A1D27'

plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'text.color':        TEXT_PRI,
    'axes.facecolor':    CARD,
    'figure.facecolor':  BG,
    'axes.edgecolor':    BORDER,
    'xtick.color':       TEXT_SEC,
    'ytick.color':       TEXT_SEC,
})

N = len(tickers)

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(10, 13), facecolor=BG)
fig.patch.set_facecolor(BG)

# Title block
fig.text(0.055, 0.965, 'IBEX 35', fontsize=26, fontweight='bold',
         color=ACCENT, va='top', fontfamily='DejaVu Sans')
fig.text(0.055, 0.940, 'Top 10 empreses per capitalització · últims 3 mesos',
         fontsize=9, color=TEXT_SEC, va='top')
fig.text(0.055, 0.923, f'Actualitzat: {datetime.today().strftime("%d %b %Y")}',
         fontsize=8, color=TEXT_SEC, va='top', alpha=0.7)

# Thin gold rule under title
rule = plt.Line2D([0.055, 0.945], [0.912, 0.912],
                  transform=fig.transFigure, color=ACCENT, lw=0.8, alpha=0.6)
fig.add_artist(rule)

# Column headers
fig.text(0.055, 0.900, 'EMPRESA',   fontsize=7, color=TEXT_SEC, va='top', fontweight='bold')
fig.text(0.310, 0.900, 'SECTOR',    fontsize=7, color=TEXT_SEC, va='top', fontweight='bold')
fig.text(0.460, 0.900, 'PREU (€)', fontsize=7, color=TEXT_SEC, va='top', fontweight='bold', ha='right')
fig.text(0.510, 0.900, '3M (%)',    fontsize=7, color=TEXT_SEC, va='top', fontweight='bold')
fig.text(0.945, 0.900, 'TENDÈNCIA', fontsize=7, color=TEXT_SEC, va='top', fontweight='bold', ha='right')

# ── Row grid ──────────────────────────────────────────────────────────────────
TOP    = 0.885
BOTTOM = 0.030
ROW_H  = (TOP - BOTTOM) / N
PAD    = 0.008

for i, (ticker, nom, sector) in enumerate(zip(tickers, noms, sectors)):
    y_top = TOP - i * ROW_H
    y_bot = y_top - ROW_H + PAD

    # Alternating row background
    row_rect = mpatches.FancyBboxPatch(
        (0.045, y_bot), 0.91, ROW_H - PAD * 0.5,
        boxstyle='round,pad=0.003',
        linewidth=0, facecolor='#161925' if i % 2 == 0 else CARD,
        transform=fig.transFigure, clip_on=False, zorder=0
    )
    fig.add_artist(row_rect)

    serie = dades[ticker].dropna()
    if len(serie) < 2:
        continue

    vals    = serie.values
    last    = vals[-1]
    first   = vals[0]
    pct     = (last - first) / first * 100
    up      = pct >= 0
    color   = GREEN if up else RED
    arrow   = '▲' if up else '▼'

    # ── Sparkline axis ────────────────────────────────────────────────────────
    row_cy = (y_top + y_bot) / 2
    ax_h   = 0.048
    ax_w   = 0.265
    ax = fig.add_axes([0.655, row_cy - ax_h / 2, ax_w, ax_h])
    ax.set_facecolor('none')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

    # Fill gradient under line
    xs = np.arange(len(vals))
    ax.fill_between(xs, vals, vals.min(), alpha=0.18, color=color, lw=0)
    ax.plot(xs, vals, color=color, linewidth=1.6, solid_capstyle='round')

    # First dot
    ax.plot(0, vals[0], 'o', color=color, markersize=3, alpha=0.5)
    # Last dot
    ax.plot(xs[-1], vals[-1], 'o', color=color, markersize=4.5,
            markeredgewidth=1.2, markeredgecolor='white')

    # Range padding
    rng = vals.max() - vals.min()
    ax.set_ylim(vals.min() - rng * 0.15, vals.max() + rng * 0.15)

    # ── Text columns ──────────────────────────────────────────────────────────
    mid_y = (y_top + y_bot) / 2

    # Index number
    fig.text(0.053, mid_y, f'{i+1:02d}', fontsize=8, color=TEXT_SEC,
             va='center', fontweight='bold')

    # Company name
    fig.text(0.085, mid_y + 0.006, nom, fontsize=9.5, color=TEXT_PRI,
             va='center', fontweight='bold')
    # Ticker
    fig.text(0.085, mid_y - 0.008, ticker.replace('.MC',''), fontsize=7,
             color=TEXT_SEC, va='center')

    # Sector badge (simulated with text box)
    fig.text(0.245, mid_y, sector, fontsize=7.2, color=ACCENT,
             va='center', fontfamily='DejaVu Sans',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#1E1A10',
                       edgecolor=ACCENT, linewidth=0.5, alpha=0.8))

    # Price
    fig.text(0.460, mid_y + 0.005, f'{last:.2f}', fontsize=10,
             color=TEXT_PRI, va='center', fontweight='bold', ha='right')
    fig.text(0.460, mid_y - 0.009, '€', fontsize=7,
             color=TEXT_SEC, va='center', ha='right')

    # % change
    fig.text(0.478, mid_y, f'{arrow} {abs(pct):.1f}%', fontsize=8.5,
             color=color, va='center', fontweight='bold')

    # Row separator line
    if i < N - 1:
        sep = plt.Line2D([0.048, 0.952],
                         [y_bot, y_bot],
                         transform=fig.transFigure,
                         color=BORDER, lw=0.5, alpha=0.5)
        fig.add_artist(sep)

# ── Footer ────────────────────────────────────────────────────────────────────
fig.text(0.055, 0.018, 'Font: Yahoo Finance  ·  Preus de tancament ajustats',
         fontsize=7, color=TEXT_SEC, alpha=0.6)
fig.text(0.945, 0.018, 'No és assessorament financer',
         fontsize=7, color=TEXT_SEC, alpha=0.4, ha='right')

out = 'sparklines_ibex35.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor=BG)
plt.close()
print(f'Saved → {out}')