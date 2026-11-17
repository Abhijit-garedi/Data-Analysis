import json
from pathlib import Path
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

st.set_page_config(
    page_title="Friendly Multi Store | Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

NAVY = "#191A4B"
PURPLE = "#4B429B"
BLUE = "#4385EF"
GREEN = "#1BA783"
RED = "#E65A68"
TEXT = "#202033"
MUTED = "#6B6B78"
BG = "#F7F8FC"

@st.cache_data
def load_data():
    transactions = pd.read_csv(DATA / "campaign_transactions.csv", parse_dates=["date"])
    product_revenue = pd.read_csv(DATA / "reported_product_revenue.csv")
    kpis = json.loads((DATA / "reported_dashboard_kpis.json").read_text(encoding="utf-8"))
    return transactions, product_revenue, kpis

transactions, product_revenue, kpis = load_data()

# Custom CSS for a dashboard-like appearance.
st.markdown("""
<style>
    .stApp { background: #F7F8FC; color: #202033; }
    .block-container { padding-top: 1.1rem; padding-bottom: 2rem; max-width: 1500px; }
    .hero {
        background: linear-gradient(115deg, #17183F 0%, #29275F 55%, #5145A0 100%);
        border-radius: 22px; padding: 28px 32px; color: white; margin-bottom: 18px;
    }
    .hero h1 { color: white; font-size: 2.1rem; margin: 0; font-weight: 800; }
    .hero .sub { color: #DADAF4; font-size: 1.02rem; letter-spacing: .08em; font-weight: 700; }
    .hero .tag { color: #D1D0EA; font-size: 1rem; margin-top: 6px; }
    .section-title { font-size: 1.25rem; font-weight: 750; color: #171717; margin: 12px 0 4px; }
    .section-sub { color: #74747D; margin-bottom: 10px; }
    .metric-card {
        border-radius: 17px; padding: 17px 20px; min-height: 112px;
        border-top: 5px solid; box-shadow: 0 1px 4px rgba(20,20,50,.04);
    }
    .metric-label { font-size: 1rem; margin-bottom: 12px; }
    .metric-value { font-size: 2rem; line-height: 1.05; font-weight: 800; }
    .metric-foot { margin-top: 5px; font-size: .9rem; }
    .panel {
        background: white; border: 1px solid #E5E6EC; border-radius: 18px;
        padding: 18px 20px; margin: 10px 0 16px;
    }
    .small-note { color: #777782; font-size: .82rem; }
    div[data-testid="stSelectbox"] label, div[data-testid="stDateInput"] label {
        color: white !important; font-weight: 650;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stDateInput"] input { border-radius: 10px; }
    .stButton button { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Header and filters.
st.markdown("""
<div class="hero">
  <div style="display:flex; gap:18px; align-items:center;">
    <div style="font-size:3.2rem;">🎮</div>
    <div>
      <h1>FRIENDLY MULTISTORE</h1>
      <div class="sub">SALES &amp; MARKETING ANALYSIS DASHBOARD</div>
      <div class="tag">Sales Performance&nbsp; | &nbsp;Product Analysis&nbsp; | &nbsp;Customer Overview</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

min_date = transactions["date"].min().date()
max_date = transactions["date"].max().date()
f1, f2, f3 = st.columns([1.2, 1.2, .55])
with f1:
    date_range = st.date_input(
        "DATE RANGE",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD MMM YYYY",
    )
with f2:
    product_options = ["All Products"] + sorted(transactions["product"].unique().tolist())
    selected_product = st.selectbox("PRODUCT", product_options)
with f3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    if st.button("↻ Reset filters", use_container_width=True):
        st.rerun()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, tuple) and len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date = end_date = date_range

filtered = transactions[
    transactions["date"].dt.date.between(start_date, end_date)
].copy()
if selected_product != "All Products":
    filtered = filtered[filtered["product"] == selected_product]

st.caption("FRIENDLY MULTISTORE · NEPAL")

# Revenue/overview metrics as reported in the supplied dashboard screenshot.
st.markdown('<div class="section-title">Sales Performance Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Reported dashboard summary · NPR</div>', unsafe_allow_html=True)

cards = [
    ("💰 Total Sales", f'{kpis["total_sales_npr"]:,}', "Nepalese Rupees", "#EEE7FF", PURPLE, "#352365"),
    ("🛒 Total Orders", f'{kpis["total_orders"]:,}', "Transactions", "#E3EDFF", BLUE, "#214B91"),
    ("📦 Quantity Sold", f'{kpis["quantity_sold"]:,}', "Units", "#DDF4EC", GREEN, "#17634F"),
    ("👥 Customers", f'{kpis["unique_customers"]:,}', "Unique customers", "#FFE5E8", RED, "#963441"),
]
cols = st.columns(4)
for col, (label, value, foot, bg, accent, color) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div class="metric-card" style="background:{bg}; border-color:{accent}; color:{color};">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-foot">{foot}</div>
        </div>
        """, unsafe_allow_html=True)

# Filtered source-data volume is kept separate from the screenshot KPI summary.
filtered_units = int(filtered["purchases"].sum()) if not filtered.empty else 0
filtered_records = int(filtered["order_id"].nunique()) if not filtered.empty else 0

left, right = st.columns([1.55, 1])
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Daily Purchase Trend")
    st.caption(f"Purchase quantities from the uploaded transaction PDF · {start_date:%d %b} – {end_date:%d %b %Y}")
    if filtered.empty:
        st.info("No transaction records match the selected filters.")
    else:
        daily = (filtered.groupby("date", as_index=False)["purchases"].sum()
                 .sort_values("date"))
        fig = px.area(daily, x="date", y="purchases", markers=True)
        fig.update_traces(line_color=BLUE, fillcolor="rgba(67,133,239,0.15)", marker=dict(size=7))
        fig.update_layout(
            height=340, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white", plot_bgcolor="white",
            xaxis_title="", yaxis_title="Purchase quantity",
            font=dict(color=MUTED), hovermode="x unified",
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(gridcolor="#E7E8ED", rangemode="tozero")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Filtered Transaction Data")
    st.metric("Purchase quantity in selected view", f"{filtered_units:,}")
    st.metric("Transaction records in selected view", f"{filtered_records:,}")
    st.metric("Products represented", f"{filtered['product'].nunique() if not filtered.empty else 0}")
    st.markdown('<div class="small-note">These figures are calculated directly from the 35-row transaction dataset.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Business insights from supplied screenshot.
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### Business Insights")
st.caption("Key performance indicators transcribed from the supplied dashboard screenshot")
insight_cols = st.columns(4)
insights = [
    ("Average Order Value", f'NPR {kpis["average_order_value_npr"]:,}'),
    ("Sales / Customer", f'NPR {kpis["sales_per_customer_npr"]:,}'),
    ("Top Product Share", f'{kpis["top_product_share_pct"]:.1f}%'),
    ("Units / Order", f'{kpis["units_per_order"]:.2f}'),
]
for c, (label, value) in zip(insight_cols, insights):
    c.markdown(f"<div style='background:#F7F7FA;border-radius:13px;padding:15px;'><div style='color:#777'>{label}</div><div style='font-size:1.45rem;font-weight:800;margin-top:5px'>{value}</div></div>", unsafe_allow_html=True)
st.markdown("**Free Fire Diamonds generated NPR 62,100** in the supplied dashboard view.")
st.markdown('</div>', unsafe_allow_html=True)

# Product revenue data from screenshots.
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### Product Performance Details")
st.caption("Revenue and contribution analysis · values transcribed from supplied screenshots")
rev_view = product_revenue.copy()
if selected_product != "All Products":
    rev_view = rev_view[rev_view["product"] == selected_product]
if rev_view.empty:
    st.info("No product revenue data available.")
else:
    display = rev_view.rename(columns={
        "product": "Product", "sales_npr": "Sales (NPR)",
        "contribution_pct": "Contribution", "rank": "Rank"
    })
    display["Sales (NPR)"] = display["Sales (NPR)"].map(lambda x: f"{x:,.0f}")
    display["Contribution"] = display["Contribution"].map(lambda x: f"{x:.1f}%")
    display["Rank"] = display["Rank"].map(lambda x: f"{x}{'st' if x == 1 else 'nd' if x == 2 else 'rd'}")
    st.dataframe(display, hide_index=True, use_container_width=True)
    fig_bar = px.bar(
        rev_view, x="product", y="sales_npr", color="product",
        color_discrete_sequence=[BLUE, "#F49A45", "#9855D9"],
        text=rev_view["sales_npr"].map(lambda x: f"{x:,.0f}")
    )
    fig_bar.update_layout(
        height=310, showlegend=False, margin=dict(l=5,r=5,t=25,b=5),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis_title="", yaxis_title="Sales (NPR)", font=dict(color=MUTED)
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_yaxes(gridcolor="#E7E8ED", rangemode="tozero")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown(f"**Best performing product:** {rev_view.sort_values('sales_npr', ascending=False).iloc[0]['product']}")
st.markdown('</div>', unsafe_allow_html=True)

# Monthly revenue chart: only one reported month is present in the supplied screenshot.
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### Monthly Sales")
st.caption("Reported total revenue in the supplied dashboard screenshot")
monthly = pd.DataFrame({"Month": ["June 2026"], "Sales (NPR)": [kpis["total_sales_npr"]]})
fig_month = px.bar(monthly, x="Month", y="Sales (NPR)", text="Sales (NPR)", color_discrete_sequence=["#665FEA"])
fig_month.update_layout(height=280, showlegend=False, margin=dict(l=10,r=10,t=20,b=10),
                        paper_bgcolor="white", plot_bgcolor="white", xaxis_title="", yaxis_title="NPR")
fig_month.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
fig_month.update_yaxes(gridcolor="#E7E8ED", rangemode="tozero")
st.plotly_chart(fig_month, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Transaction table and source-data transparency.
with st.expander("View source transaction records"):
    view = filtered.sort_values(["date", "order_id"]).copy()
    view["date"] = view["date"].dt.strftime("%d %b %Y")
    st.dataframe(view, hide_index=True, use_container_width=True)
    st.download_button(
        "Download filtered transactions as CSV",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="friendly_multistore_filtered_transactions.csv",
        mime="text/csv",
    )

st.markdown("""
<div class="small-note" style="padding:8px 2px 20px;">
<strong>Data note:</strong> The uploaded transaction PDF contains 35 order records and 200 total purchase units
(Free Fire Diamonds 168, PUBG UC 31, Mobile Legends 1). The revenue and overview KPIs above are separately
transcribed from the dashboard screenshots supplied for this project. They are not derivable from the PDF's
purchase-quantity-only records. The date and product filters apply to the source transaction records and the
daily purchase trend.
</div>
""", unsafe_allow_html=True)
