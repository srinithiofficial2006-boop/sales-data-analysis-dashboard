"""Sales Analytics Dashboard (Streamlit, dark navy and electric blue).

Run from the project root:
    streamlit run dashboard/app.py
Needs .streamlit/config.toml (dark navy theme) in the project root.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Sales Analytics", page_icon="📊", layout="wide",
                   initial_sidebar_state="collapsed")

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "cleaned_sales_data.csv"

# ---------- design tokens (dark navy + electric blue) ----------
BG, SURFACE, SURFACE2 = "#0B1220", "#111827", "#172338"
LINE, GRID = "#263A57", "#20314A"
INK, INK2, INK3 = "#F8FAFC", "#CBD5E1", "#94A3B8"
BLUE, ORANGE, AQUA, YELLOW = "#3B82F6", "#F59E0B", "#10B981", "#FBBF24"
CAT_ORDER = ["Accessories", "Electronics", "Furniture", "Office Supplies"]
CAT_COLORS = dict(zip(CAT_ORDER, [BLUE, ORANGE, AQUA, YELLOW]))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
html, body, .stApp, [class*="css"] { font-family:'IBM Plex Sans',system-ui,sans-serif; }
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], header, footer { display:none !important; }
.block-container { max-width:1400px; padding:1.6rem 1.5rem 3rem; }

.stApp { background:#0B1220; color:#F8FAFC; }
.banner { display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; background:linear-gradient(120deg,#172B4D 0%,#0B1220 100%); border:1px solid #263A57; border-radius:14px; padding:18px 22px; margin-bottom:1.1rem; box-shadow:0 6px 24px rgba(0,0,0,.22); }
.brand { display:flex; align-items:center; gap:12px; }
.logo { width:38px; height:38px; border-radius:10px; background:#2563EB; display:grid; place-items:center; }
.title { font-size:21px; font-weight:700; letter-spacing:-.01em; color:#F8FAFC; line-height:1.2; }
.sub { color:#93C5FD; font-size:12.5px; }
.pill { font-family:ui-monospace,Menlo,monospace; font-size:12px; color:#BFDBFE; background:#172B4D; border:1px solid #3B82F6; border-radius:999px; padding:6px 12px; }

.lab { font-size:11px; font-weight:600; letter-spacing:.07em; text-transform:uppercase; color:#94A3B8; margin-bottom:4px; }
[data-testid="stPills"] button { border-radius:8px !important; font-size:13px !important; }
[data-testid="stDateInput"] input { font-size:13px; }
.stButton > button, .stDownloadButton > button { border-radius:8px; border:1px solid #263A57; background:#172338; color:#F8FAFC; }
.stButton > button:hover, .stDownloadButton > button:hover { background:#1D4ED8; border-color:#60A5FA; color:#FFFFFF; }
hr { border-color:#263A57; margin:.6rem 0 1rem; }

.kpi { box-shadow:0 4px 16px rgba(0,0,0,.15); min-height:112px; background:#111827; border:1px solid #263A57; border-radius:12px; padding:15px 16px; overflow:hidden; white-space:nowrap; }
.kpi .k { font-size:11.5px; font-weight:600; letter-spacing:.06em; text-transform:uppercase; color:#94A3B8; }
.kpi .v { font-size:26px; font-weight:700; letter-spacing:-.02em; margin:6px 0 2px; color:#F8FAFC; }
.kpi .s { font-size:12px; color:#94A3B8; }
.kpi.hero { background:linear-gradient(135deg,#2563EB,#1D4ED8); border-color:#3B82F6; }
.kpi.hero .k, .kpi.hero .s { color:#DBEAFE; } .kpi.hero .v { color:#FFFFFF; }

[class*="st-key-card_"] { box-shadow:0 4px 16px rgba(0,0,0,.15); background:#111827; border:1px solid #263A57 !important; border-radius:12px; padding:14px 16px 6px; }
.ct { font-size:14.5px; font-weight:600; color:#F8FAFC; margin:0; }
.ch { font-size:12px; color:#94A3B8; margin:2px 0 4px; }
.ins { background:#111827; border:1px solid #263A57; border-radius:12px; padding:14px 16px; }
.ins .k { font-size:11px; font-weight:600; letter-spacing:.07em; text-transform:uppercase; color:#94A3B8; }
.ins .v { font-size:17px; font-weight:600; margin:5px 0 2px; color:#60A5FA; }
.ins .s { font-size:12.5px; color:#CBD5E1; }
div[data-testid="stDataFrame"] { border:1px solid #263A57; border-radius:10px; }
[data-baseweb="select"] > div, [data-testid="stDateInput"] > div > div { background:#111827; border-color:#263A57; color:#F8FAFC; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(path: str, modified: float) -> pd.DataFrame:
    df = pd.read_csv(path)
    need = ["Order_ID", "Order_Date", "Customer_Name", "Product", "Category", "Region", "State",
            "Quantity", "Discount", "Sales", "Cost", "Profit"]
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for c in ["Quantity", "Discount", "Sales", "Cost", "Profit"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["Order_Date", "Sales"]).copy()
    df[["Quantity", "Discount", "Cost", "Profit"]] = df[["Quantity", "Discount", "Cost", "Profit"]].fillna(0)
    df["Month"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()
    return df


if not DATA_FILE.exists():
    st.error(f"Data file not found: {DATA_FILE}")
    st.stop()
try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load data: {exc}")
    st.stop()
if df.empty:
    st.warning("The dataset has no usable records.")
    st.stop()


def inr(v: float) -> str:
    return f"₹{v:,.0f}"


def short(v: float) -> str:
    a = abs(v)
    if a >= 1e7: return f"₹{v/1e7:.2f} Cr"
    if a >= 1e5: return f"₹{v/1e5:.2f} L"
    if a >= 1e3: return f"₹{v/1e3:.1f}K"
    return f"₹{v:.0f}"


def tick_fmt(v: float) -> str:
    a = abs(v)
    if a >= 1e7: return f"{v/1e7:g} Cr"
    if a >= 1e5: return f"{v/1e5:g} L"
    if a >= 1e3: return f"{v/1e3:g}K"
    return f"{v:g}"


def nice_step(top: float, n: int = 5) -> float:
    raw = max(top / n, 1)
    mag = 10 ** (len(str(int(raw))) - 1)
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= raw:
            return m * mag
    return 10 * mag


def money_ticks(fig: go.Figure, axis: str, vals) -> None:
    top = float(max(vals)) if len(vals) else 1.0
    step = nice_step(top)
    ticks = [step * i for i in range(int(top / step) + 2)]
    (fig.update_yaxes if axis == "y" else fig.update_xaxes)(
        tickvals=ticks, ticktext=[tick_fmt(t) for t in ticks], range=[0, ticks[-1]])


def style(fig: go.Figure, h: int = 320, legend: bool = False) -> go.Figure:
    fig.update_layout(
        height=h, margin=dict(l=8, r=12, t=8, b=8), paper_bgcolor=BG, plot_bgcolor=SURFACE,
        font=dict(family="IBM Plex Sans, sans-serif", color=INK2, size=12), showlegend=legend,
        legend=dict(orientation="h", y=1.1, x=1, xanchor="right", font=dict(color=INK2, size=12)),
        hoverlabel=dict(bgcolor=SURFACE2, bordercolor=LINE, font=dict(color=INK)), bargap=0.35)
    fig.update_xaxes(showgrid=False, linecolor=LINE, automargin=True, tickfont=dict(color=INK3, size=11))
    fig.update_yaxes(gridcolor=GRID, zeroline=False, automargin=True, tickfont=dict(color=INK3, size=11))
    return fig


def show(fig: go.Figure) -> None:
    st.plotly_chart(fig, width="stretch", theme=None, config={"displayModeBar": False})


def head(t: str, hint: str) -> None:
    st.markdown(f'<div class="ct">{t}</div><div class="ch">{hint}</div>', unsafe_allow_html=True)


cats = sorted(df["Category"].unique())
regs = sorted(df["Region"].unique())
dmin, dmax = df["Order_Date"].min().date(), df["Order_Date"].max().date()


def reset_filters() -> None:
    st.session_state["cat"] = cats
    st.session_state["reg"] = regs
    st.session_state["dates"] = (dmin, dmax)


for key, default in (("cat", cats), ("reg", regs), ("dates", (dmin, dmax))):
    st.session_state.setdefault(key, default)

dates = st.session_state["dates"]
start, end = (dates[0], dates[1]) if isinstance(dates, (tuple, list)) and len(dates) == 2 else (dmin, dmin if not dates else dates[0] if isinstance(dates, (tuple, list)) else dates)
if isinstance(dates, (tuple, list)) and len(dates) == 1:
    start = end = dates[0]

st.markdown(
    '<div class="banner"><div class="brand"><div class="logo"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" '
    'stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/></svg></div>'
    '<div><div class="title">Sales Analytics</div>'
    f'<div class="sub">Cleaned sales data · {len(df):,} orders · all amounts in ₹</div></div></div>'
    f'<span class="pill">{start:%d %b %Y} – {end:%d %b %Y}</span></div>', unsafe_allow_html=True)

fc1, fc2, fc3, fc4 = st.columns([3, 2.6, 2.2, 1], vertical_alignment="bottom")
with fc1:
    st.markdown('<div class="lab">Category</div>', unsafe_allow_html=True)
    sel_cats = st.pills("Category", cats, selection_mode="multi", key="cat", label_visibility="collapsed") or []
with fc2:
    st.markdown('<div class="lab">Region</div>', unsafe_allow_html=True)
    sel_regs = st.pills("Region", regs, selection_mode="multi", key="reg", label_visibility="collapsed") or []
with fc3:
    st.markdown('<div class="lab">Order date</div>', unsafe_allow_html=True)
    st.date_input("Order date", key="dates", min_value=dmin, max_value=dmax, format="DD/MM/YYYY", label_visibility="collapsed")
with fc4:
    st.button("Reset filters", on_click=reset_filters, width="stretch")
st.divider()

f = df[df["Category"].isin(sel_cats) & df["Region"].isin(sel_regs)
       & (df["Order_Date"].dt.date >= start) & (df["Order_Date"].dt.date <= end)].copy()
if f.empty:
    st.warning("No orders match the filters. Select more categories or regions, or widen the date range.")
    st.stop()

sales, profit, cost = f["Sales"].sum(), f["Profit"].sum(), f["Cost"].sum()
orders, units, custs = f["Order_ID"].nunique(), f["Quantity"].sum(), f["Customer_Name"].nunique()
cards = [
    ("Total sales", short(sales), inr(sales), True),
    ("Total profit", short(profit), f"Cost {short(cost)}", False),
    ("Orders", f"{orders:,}", f"{units:,.0f} units sold", False),
    ("Avg order value", short(sales / orders), f"Across {custs} customers", False),
    ("Profit margin", f"{profit / sales * 100:.1f}%", "Profit ÷ sales", False),
    ("Avg discount", f"{f['Discount'].mean() * 100:.1f}%", "Per order", False),
]
for col, (k, v, s, hero) in zip(st.columns(6), cards):
    col.markdown(f'<div class="kpi{" hero" if hero else ""}"><div class="k">{k}</div>'
                 f'<div class="v">{v}</div><div class="s">{s}</div></div>', unsafe_allow_html=True)
st.write("")

# ---------- row 1 ----------
c1, c2 = st.columns([2, 1], gap="medium")
with c1:
    with st.container(border=True, key="card_1"):
        head("Monthly sales and profit", "Both measures in ₹, same scale")
        m = f.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        fig = go.Figure()
        fig.add_scatter(x=m["Month"], y=m["Sales"], name="Sales", mode="lines+markers",
                        line=dict(color=BLUE, width=2.5, shape="spline", smoothing=.6),
                        marker=dict(size=7, color=BLUE, line=dict(color=SURFACE, width=1.5)),
                        fill="tozeroy", fillcolor="rgba(59,130,246,.16)",
                        hovertemplate="%{x|%b %Y}<br>Sales ₹%{y:,.0f}<extra></extra>")
        fig.add_scatter(x=m["Month"], y=m["Profit"], name="Profit", mode="lines+markers",
                        line=dict(color=AQUA, width=2.5, shape="spline", smoothing=.6),
                        marker=dict(size=7, color=AQUA, line=dict(color=SURFACE, width=1.5)),
                        hovertemplate="%{x|%b %Y}<br>Profit ₹%{y:,.0f}<extra></extra>")
        style(fig, 340, legend=True).update_xaxes(tickformat="%b '%y", dtick="M2")
        money_ticks(fig, "y", m["Sales"])
        show(fig)
with c2:
    with st.container(border=True, key="card_2"):
        head("Sales by category", "Share of total sales")
        c = f.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
        labels = [f"{n} · {v / c['Sales'].sum() * 100:.0f}%" for n, v in zip(c["Category"], c["Sales"])]
        fig = go.Figure(go.Pie(labels=labels, values=c["Sales"], hole=.64, sort=False,
                               marker=dict(colors=[CAT_COLORS.get(x, INK3) for x in c["Category"]],
                                           line=dict(color=SURFACE, width=2)),
                               textinfo="none", hovertemplate="%{label}<br>₹%{value:,.0f}<extra></extra>"))
        style(fig, 340, legend=True).update_layout(legend=dict(orientation="h", y=-0.02, x=.5, xanchor="center",
                                                               font=dict(color=INK2, size=12)))
        show(fig)

# ---------- row 2 ----------
c3, c4 = st.columns(2, gap="medium")
with c3:
    with st.container(border=True, key="card_3"):
        head("Sales and profit by region", "Total ₹ per region")
        r = f.groupby("Region", as_index=False)[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False)
        fig = go.Figure()
        fig.add_bar(x=r["Region"], y=r["Sales"], name="Sales", marker_color=BLUE,
                    hovertemplate="%{x}<br>Sales ₹%{y:,.0f}<extra></extra>")
        fig.add_bar(x=r["Region"], y=r["Profit"], name="Profit", marker_color=AQUA,
                    hovertemplate="%{x}<br>Profit ₹%{y:,.0f}<extra></extra>")
        style(fig, 320, legend=True).update_layout(barmode="group")
        money_ticks(fig, "y", r["Sales"])
        show(fig)
with c4:
    with st.container(border=True, key="card_4"):
        head("Top products by sales", "Ranked by total ₹")
        p = f.groupby("Product", as_index=False)["Sales"].sum().nlargest(8, "Sales").sort_values("Sales")
        fig = go.Figure(go.Bar(x=p["Sales"], y=p["Product"], orientation="h", marker_color=BLUE,
                               hovertemplate="%{y}<br>₹%{x:,.0f}<extra></extra>"))
        style(fig, 320).update_xaxes(showgrid=True, gridcolor=GRID).update_yaxes(showgrid=False)
        money_ticks(fig, "x", p["Sales"])
        show(fig)

# ---------- row 3 ----------
c5, c6 = st.columns(2, gap="medium")
with c5:
    with st.container(border=True, key="card_5"):
        head("Profit margin by category", "Profit as % of sales")
        g = f.groupby("Category")[["Sales", "Profit"]].sum()
        g["Margin"] = g["Profit"] / g["Sales"] * 100
        g = g.sort_values("Margin", ascending=False).reset_index()
        fig = go.Figure(go.Bar(x=g["Category"], y=g["Margin"], marker_color=[CAT_COLORS.get(x, INK3) for x in g["Category"]],
                               hovertemplate="%{x}<br>%{y:.2f}%<extra></extra>"))
        style(fig, 320).update_yaxes(ticksuffix="%", rangemode="tozero")
        show(fig)
with c6:
    with st.container(border=True, key="card_6"):
        head("Sales by state", "Top states by total ₹")
        s = f.groupby("State", as_index=False)["Sales"].sum().nlargest(8, "Sales").sort_values("Sales")
        fig = go.Figure(go.Bar(x=s["Sales"], y=s["State"], orientation="h", marker_color=BLUE,
                               hovertemplate="%{y}<br>₹%{x:,.0f}<extra></extra>"))
        style(fig, 320).update_xaxes(showgrid=True, gridcolor=GRID).update_yaxes(showgrid=False)
        money_ticks(fig, "x", s["Sales"])
        show(fig)

# ---------- insights ----------
top_cat = f.groupby("Category")["Sales"].sum().sort_values(ascending=False)
top_reg = f.groupby("Region")["Sales"].sum().sort_values(ascending=False)
top_prod = f.groupby("Product")["Sales"].agg(["sum", "count"]).sort_values("sum", ascending=False)
top_month = f.groupby("Month")["Sales"].sum().sort_values(ascending=False)
ins = [
    ("Top category", top_cat.index[0], f"{short(top_cat.iloc[0])} · {top_cat.iloc[0] / sales * 100:.0f}% of sales"),
    ("Leading region", top_reg.index[0], f"{short(top_reg.iloc[0])} · {top_reg.iloc[0] / sales * 100:.0f}% of sales"),
    ("Best-selling product", top_prod.index[0], f"{short(top_prod['sum'].iloc[0])} · {int(top_prod['count'].iloc[0])} orders"),
    ("Peak month", f"{top_month.index[0]:%b '%y}", f"{short(top_month.iloc[0])} in sales"),
]
for col, (k, v, s_) in zip(st.columns(4), ins):
    col.markdown(f'<div class="ins"><div class="k">{k}</div><div class="v">{v}</div><div class="s">{s_}</div></div>',
                 unsafe_allow_html=True)
st.write("")


with st.container(border=True, key="card_7"):
    t1, t2 = st.columns([3, 1.4], vertical_alignment="bottom")
    q = t2.text_input("Search", placeholder="Search product, customer, order ID…", label_visibility="collapsed")
    t = f
    if q.strip():
        mask = pd.Series(False, index=t.index)
        for col in ["Order_ID", "Customer_Name", "Product", "State"]:
            mask |= t[col].astype(str).str.contains(q.strip(), case=False, na=False)
        t = t[mask]
    t1.markdown(f'<div class="ct">Orders</div><div class="ch">{len(t):,} orders shown</div>', unsafe_allow_html=True)
    show_cols = [c for c in ["Order_ID", "Order_Date", "Customer_Name", "Product", "Category", "Region", "State",
                             "Quantity", "Sales", "Profit", "Payment_Method"] if c in t.columns]
    st.dataframe(t[show_cols].sort_values("Order_Date", ascending=False), width="stretch", hide_index=True, height=420,
                 column_config={"Order_Date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
                                "Sales": st.column_config.NumberColumn("Sales", format="₹%d"),
                                "Profit": st.column_config.NumberColumn("Profit", format="₹%d")})
    st.download_button("Download filtered CSV", t.drop(columns=["Month"]).to_csv(index=False).encode("utf-8-sig"),
                       "sales_filtered.csv", "text/csv")