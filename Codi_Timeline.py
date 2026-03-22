"""
Línia de Temps: Cursa Espacial — dades de Wikipedia
Font: https://en.wikipedia.org/wiki/Timeline_of_the_Space_Race
Exporta → timeline_cursa_espacial.png (300 dpi)
"""

import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import textwrap
from datetime import datetime
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# 1. CÀRREGA DE DADES DES DE WIKIPEDIA
# ══════════════════════════════════════════════════════════════════════════════
url = "https://en.wikipedia.org/wiki/Timeline_of_the_Space_Race"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
html = response.text
tables = pd.read_html(StringIO(html))

# Taula índex 2 → periode 1957–1959
df_raw = tables[2].dropna(how="all").copy()

# ── Normalitza noms de columnes ───────────────────────────────────────────────
# Les columnes habituals de Wikipedia són:
#   "Date", "Country", "Achievement", "Mission / Vehicle" (o similars)
df_raw.columns = [str(c).strip() for c in df_raw.columns]

# ── Detecta la columna de data, país i descripció ────────────────────────────
# Busquem de forma flexible per si Wikipedia canvia lleugerament els noms
col_date    = next((c for c in df_raw.columns if "date" in c.lower()), df_raw.columns[0])
col_country = next((c for c in df_raw.columns if "country" in c.lower()), None)
col_achiev  = next((c for c in df_raw.columns if "achiev" in c.lower()
                    or "event" in c.lower() or "description" in c.lower()), None)
col_mission = next((c for c in df_raw.columns if "mission" in c.lower()
                    or "vehicle" in c.lower() or "spacecraft" in c.lower()), None)

# ── Neteja i parse de dates ───────────────────────────────────────────────────
df = df_raw[[col_date, col_country, col_achiev, col_mission]].copy()
df.columns = ["Data_raw", "Nació", "Fita", "Missió"]

df["Nació"] = df["Nació"].astype(str).str.strip().str.upper()
df["Nació"] = df["Nació"].replace({
    "SOVIET UNION": "URSS", "USSR": "URSS",
    "UNITED STATES": "EUA",  "USA":  "EUA",
    "US":            "EUA",
})

# Filtra només URSS i EUA
df = df[df["Nació"].isin(["URSS", "EUA"])].copy()

# Parse de data (format Wikipedia: "1957 August 21" o similar)
def parse_data_wiki(s):
    s = str(s).strip()
    for fmt in ("%Y %B %d", "%d %B %Y", "%B %d, %Y", "%Y-%m-%d", "%B %Y"):
        try:
            return pd.to_datetime(s, format=fmt)
        except ValueError:
            pass
    try:
        return pd.to_datetime(s)   # fallback genèric
    except Exception:
        return pd.NaT

df["Data"] = df["Data_raw"].apply(parse_data_wiki)
df = df.dropna(subset=["Data"]).sort_values("Data").reset_index(drop=True)

# ── Trunca la fita per a visualitzar-la neta ─────────────────────────────────
def trunca(text, max_c=100):
    import re
    t = str(text).strip()
    # Talla a partir de la segona aparició de "First"
    m = re.search(r"(?i)(first\s+\S.+?)\s+(first\s)", t)
    if m:
        t = t[:m.start(2)].strip().rstrip(".")
    return t if len(t) <= max_c else t[:max_c].rstrip() + "…"

df["Títol"]    = df["Missió"].apply(lambda x: str(x).strip())
df["Subtítol"] = df["Fita"].apply(trunca)

# ── Assigna alçades alternades automàticament ────────────────────────────────
# Alterna amunt/avall i varia l'amplitud per evitar solapaments
ALÇADES_AMUNT  = [0.82, 0.35, 0.42, 0.80, 0.3, 0.85, 0.30, 0.78, 0.38]
ALÇADES_AVALL  = [-0.25, -0.70, -0.5, -0.60, -0.25, -0.75, -0.28, -0.82, -0.42]

alçades = []
idx_up, idx_dn = 0, 0
for i in range(len(df)):
    if i % 2 == 0:
        alçades.append(ALÇADES_AMUNT[idx_up % len(ALÇADES_AMUNT)])
        idx_up += 1
    else:
        alçades.append(ALÇADES_AVALL[idx_dn % len(ALÇADES_AVALL)])
        idx_dn += 1
df["Alçada"] = alçades

# ══════════════════════════════════════════════════════════════════════════════
# 2. VISUALITZACIÓ
# ══════════════════════════════════════════════════════════════════════════════

plt.rcParams.update({
    "font.family":        "serif",
    "font.serif":         ["Georgia", "Times New Roman", "DejaVu Serif"],
    "axes.unicode_minus": False,
})

# Paleta
C_USSR     = "#e05252"
C_USA      = "#4a9eda"
C_LINE     = "#5b8db8"
C_BG       = "#0a1628"
C_GRID     = "#1a3050"
C_SUB      = "#8fa8bd"
C_STARS    = "#ffffff"
BBOX_ALPHA = 0.9

df["Color"] = df["Nació"].map({"URSS": C_USSR, "EUA": C_USA})

# ── Rang temporal ajustat a les dades reals ──────────────────────────────────
data_min = df["Data"].min()
data_max = df["Data"].max()
any_min  = data_min.year
any_max  = data_max.year

rang_dies = (data_max - data_min).days
marge     = pd.Timedelta(days=max(int(rang_dies * 0.08), 90))

DATA_INICI = data_min - marge
DATA_FI    = data_max + marge

# ── Figura ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 11), facecolor=C_BG)
ax.set_facecolor(C_BG)
ax.set_xlim(DATA_INICI, DATA_FI)
ax.set_ylim(-1.10, 1.18)

for espina in ax.spines.values():
    espina.set_visible(False)
ax.get_yaxis().set_visible(False)

# ── Estrelles ─────────────────────────────────────────────────────────────────
rng = np.random.default_rng(42)
n   = 320
sx  = [DATA_INICI + (DATA_FI - DATA_INICI) * t for t in rng.uniform(0, 1, n)]
sy  = rng.uniform(-1.05, 1.15, n)
ax.scatter(sx, sy, s=rng.uniform(0.4, 4.5, n),
           c=C_STARS, alpha=rng.uniform(0.10, 0.50, n), zorder=0, linewidths=0)

# ── Graella ───────────────────────────────────────────────────────────────────
anys_graella = range(any_min - (any_min % 2), any_max + 4, 2)
for any_ in anys_graella:
    ax.axvline(datetime(any_, 1, 1), color=C_GRID,
               linewidth=0.6, linestyle="--", zorder=1, alpha=0.50)

# ── Línia temporal ────────────────────────────────────────────────────────────
ax.plot([DATA_INICI, DATA_FI], [0, 0],
        color=C_LINE, linewidth=3.0, solid_capstyle="round", zorder=3)
ax.annotate("",
    xy=(DATA_FI, 0), xytext=(DATA_FI - pd.Timedelta(days=200), 0),
    arrowprops=dict(arrowstyle="-|>", color=C_SUB, lw=2, mutation_scale=16),
    zorder=4)

# ── Helper: subtítol en múltiples línies ──────────────────────────────────────
def wrap_text(text, max_chars=24):
    return "\n".join(textwrap.wrap(str(text).strip(), width=max_chars))

# ── Dibuixa cada fita ─────────────────────────────────────────────────────────
for _, row in df.iterrows():
    x  = row["Data"]
    h  = row["Alçada"]
    c  = row["Color"]
    up = h > 0
    sign = 1 if up else -1
    va   = "bottom" if up else "top"

    # Tija puntejada
    ax.plot([x, x], [sign * 0.05, h - sign * 0.08],
            color=c, linewidth=1.5, alpha=0.55,
            zorder=2, linestyle=(0, (5, 3)))

    # Punt a la línia (halo + anell + centre)
    ax.scatter(x, 0, s=320, color=C_BG,    zorder=5, linewidths=0, alpha=0.9)
    ax.scatter(x, 0, s=200, color=c,       zorder=6, edgecolors="white", linewidths=1.8)
    ax.scatter(x, 0, s=55,  color="white", zorder=7, linewidths=0)

    # Punt al cap de la tija
    ax.scatter(x, h, s=90, color=c, zorder=6, edgecolors="white", linewidths=1.5)

    # ── Etiqueta de data: "Any\nMes" ──────────────────────────────────────────
    mes_curt = x.strftime("%b")   # Jan, Feb, Mar...
    data_label = f"{x.year}\n{mes_curt}"
    ax.text(x, sign * 0.072, data_label,
            ha="center", va=va,
            color=c, fontsize=10, fontweight="bold",
            linespacing=1.25, zorder=9,
            bbox=dict(boxstyle="round,pad=0.28",
                      fc=C_BG, ec=c, alpha=0.90, lw=1.0))

    # ── Títol (nom missió) ────────────────────────────────────────────────────
    ax.text(x, h + sign * 0.072, row["Títol"],
            ha="center", va=va,
            color="white", fontsize=14.5, fontweight="bold", zorder=9,
            bbox=dict(boxstyle="round,pad=0.38",
                      fc="#000000", ec=c, alpha=BBOX_ALPHA, lw=1.5))

    # ── Subtítol multilínia ───────────────────────────────────────────────────
    sub_wrapped = wrap_text(row["Subtítol"], max_chars=24)
    n_lines = sub_wrapped.count("\n") + 1
    # Desplaçament dinàmic: títol (0.072) + altura del títol (~0.10) + gap (0.04)
    dy_sub = sign * (0.072 + 0.105 + 0.040)
    ax.text(x, h + dy_sub, sub_wrapped,
            ha="center", va=va,
            color=c, fontsize=12, fontweight="bold",
            fontfamily="DejaVu Sans",
            linespacing=1.45, zorder=9,
            bbox=dict(boxstyle="round,pad=0.32",
                      fc="#000000", ec=c, lw=0.9))

    # ── Badge nació ───────────────────────────────────────────────────────────
    # Desplaçament: dy_sub + alçada del subtítol (proporcional a n_lines)
    dy_nacio = dy_sub + sign * (0.06 * n_lines + 0.035)
    ax.text(x, h + dy_nacio, f"▸ {row['Nació']}",
            ha="center", va=va,
            color=c, fontsize=9.5, fontweight="bold", zorder=9,
            bbox=dict(boxstyle="round,pad=0.24", fc=c, ec="none", alpha=0.20))

# ── Eix X ─────────────────────────────────────────────────────────────────────
rang_anys = any_max - any_min
if rang_anys <= 3:
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
elif rang_anys <= 8:
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
else:
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

ax.tick_params(axis="x", labelsize=12, colors=C_SUB, length=5, width=1.0, pad=8)
for etiq in ax.get_xticklabels():
    etiq.set_fontweight("bold")

# ── Llegenda — ancorada a la figura (no a l'eix), zona superior dreta ─────────
patch_urss = mpatches.Patch(facecolor=C_USSR, edgecolor="white", lw=0.8,
                             label="Unió Soviètica (URSS)")
patch_eua  = mpatches.Patch(facecolor=C_USA,  edgecolor="white", lw=0.8,
                             label="Estats Units (EUA)")
legend = fig.legend(
    handles=[patch_urss, patch_eua],
    loc="upper right",
    bbox_to_anchor=(0.98, 0.92),   # coordenades de figura: x=98%, y=88%
    fontsize=12, frameon=True,
    facecolor="#07101e", edgecolor="#2a4a6a", framealpha=0.97,
    handlelength=1.3, borderpad=1.0, labelspacing=0.75,
    labelcolor="#dfe6e9",
)
legend.get_frame().set_linewidth(1.3)

# ── Títols ────────────────────────────────────────────────────────────────────
periode = f"{any_min} - {any_max}"
fig.text(0.5, 0.97, "LA CURSA ESPACIAL",
         ha="center", va="top", fontsize=28, fontweight="bold",
         color="white", fontfamily="serif")
fig.text(0.5, 0.905,
         f"Les fites que van definir la rivalitat entre la URSS i els EUA  ·  {periode}",
         ha="center", va="top", fontsize=12.5, color=C_SUB, style="italic")
fig.text(0.5, 0.012,
         "Font: Wikipedia - Timeline of the Space Race",
         ha="center", va="bottom", fontsize=8.5, color="#3d607a")

plt.tight_layout(rect=[0, 0.02, 1, 0.88])

arxiu = "timeline_cursa_espacial.png"
plt.savefig(arxiu, dpi=1200, bbox_inches="tight", facecolor=C_BG)
plt.show()