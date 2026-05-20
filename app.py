import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UK Retail Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  THEME & GLOBAL CSS
# ─────────────────────────────────────────────
BG        = "#0d0f1e"
CARD      = "#131629"
SIDEBAR   = "#0a0c18"
BORDER    = "#1e2240"
ACCENT    = "#6c63ff"
ACCENT2   = "#4fc978"
ACCENT3   = "#f9a03f"
TEXT      = "#e2e4f0"
MUTED     = "#7b7f9e"

st.markdown(f"""
<style>
    /* ── Hide Streamlit chrome ── */
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    #MainMenu, footer {{ display: none !important; }}

    /* ── Base ── */
    html, body, .stApp {{
        background-color: {BG} !important;
        color: {TEXT};
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}

    /* ── Remove default block padding ── */
    .block-container {{
        padding: 1.5rem 2rem 2rem 2rem !important;
        max-width: 100% !important;
    }}

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR} !important;
        border-right: 1px solid {BORDER};
        padding-top: 1.5rem;
    }}
    section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

    /* ── Sidebar filter labels ── */
    section[data-testid="stSidebar"] label {{
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: {MUTED} !important;
        margin-bottom: 4px !important;
    }}

    /* ── Multiselect container ── */
    div[data-testid="stMultiSelect"] > div {{
        background-color: #1a1c2e !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
    }}
    ul[data-testid="stMultiSelectList"] li:hover,
    div[data-baseweb="popover"] li:hover {{
        background-color: {ACCENT}22 !important;
    }}

    /* ── Slider ── */
    div[data-testid="stSlider"] label {{
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: {MUTED} !important;
    }}

    /* ── Typography ── */
    h1, h2, h3, h4, h5, h6 {{ color: {TEXT} !important; }}
    p, label, span, div {{ color: {TEXT}; }}
    hr {{ border-color: {BORDER}; margin: 1.5rem 0; }}

    /* ── Chart card wrapper ── */
    .chart-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 1.2rem 1.4rem 0.6rem 1.4rem;
        margin-bottom: 1.2rem;
    }}

    /* ── Section heading ── */
    .section-heading {{
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {MUTED};
        margin-bottom: 0.8rem;
    }}

    /* ── Expander ── */
    div[data-testid="stExpander"] {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}
    div[data-testid="stExpander"] summary {{
        color: {TEXT} !important;
        background-color: {CARD};
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    div[data-testid="stExpander"] summary:hover {{ background-color: #1e2140; }}
    div[data-testid="stExpander"] summary svg {{ fill: {MUTED} !important; }}
    div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {{
        background-color: {CARD};
        border-top: 1px solid {BORDER};
    }}

    /* ── Download button ── */
    div[data-testid="stDownloadButton"] button {{
        background-color: {ACCENT}22 !important;
        color: {TEXT} !important;
        border: 1px solid {ACCENT}55 !important;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    div[data-testid="stDownloadButton"] button:hover {{
        background-color: {ACCENT}44 !important;
        border-color: {ACCENT} !important;
    }}

    /* ── Dataframe ── */
    .dataframe {{ color: {TEXT} !important; }}
    div[data-testid="stDataFrame"] {{ border-radius: 10px; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def chart_layout(fig, height=340):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=TEXT,
        font_family="Inter, Segoe UI, sans-serif",
        title_font_size=14,
        title_font_color=TEXT,
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        xaxis=dict(gridcolor=BORDER, zeroline=False),
        yaxis=dict(gridcolor=BORDER, zeroline=False),
    )
    return fig

def card(fig):
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOAD & CACHE DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("online_retail_II.csv", encoding="latin1")
    df = df.dropna(subset=["Customer ID"])
    df = df[~df["Invoice"].astype(str).str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalPrice"]  = df["Quantity"] * df["Price"]
    df["Year"]        = df["InvoiceDate"].dt.year
    df["Month"]       = df["InvoiceDate"].dt.month
    df["Month_Name"]  = df["InvoiceDate"].dt.strftime("%B")
    df["Day_of_Week"] = df["InvoiceDate"].dt.strftime("%A")
    df["Hour"]        = df["InvoiceDate"].dt.hour
    df["Customer ID"] = df["Customer ID"].astype(str)
    return df


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def sidebar_filters(df):
    st.sidebar.markdown(f"""
        <div style="padding: 0 0.5rem 1.2rem 0.5rem;">
            <div style="font-size:1.3rem; font-weight:700; color:{TEXT}; letter-spacing:-0.02em;">
                UK Retail
            </div>
            <div style="font-size:0.72rem; color:{MUTED}; font-weight:500;
                        letter-spacing:0.08em; text-transform:uppercase; margin-top:2px;">
                Sales Intelligence
            </div>
        </div>
        <div style="height:1px; background:{BORDER}; margin-bottom:1.4rem;"></div>
        <div style="font-size:0.65rem; font-weight:700; letter-spacing:0.12em;
                    text-transform:uppercase; color:{MUTED}; margin-bottom:0.5rem;">
            Filters
        </div>
    """, unsafe_allow_html=True)

    years = sorted(df["Year"].unique())
    selected_years = st.sidebar.multiselect("Year(s)", years, default=years)

    countries = sorted(df["Country"].unique())
    selected_countries = st.sidebar.multiselect(
        "Country(ies)", countries, default=["United Kingdom"]
    )

    top_n = st.sidebar.slider("Top N Products", 5, 20, 10)

    st.sidebar.markdown(f"""
        <div style="height:1px; background:{BORDER}; margin:1.4rem 0 1rem 0;"></div>
        <div style="font-size:0.72rem; color:{MUTED}; line-height:1.9;">
            <div>Dataset &nbsp;·&nbsp; UCI Online Retail II</div>
            <div>Stack &nbsp;·&nbsp; Python · Streamlit · Plotly</div>
        </div>
    """, unsafe_allow_html=True)

    return selected_years, selected_countries, top_n


# ─────────────────────────────────────────────
#  KPI CARDS
# ─────────────────────────────────────────────
def show_kpis(df):
    total_revenue   = df["TotalPrice"].sum()
    total_orders    = df["Invoice"].nunique()
    total_customers = df["Customer ID"].nunique()
    total_products  = df["Description"].nunique()
    avg_order_value = df.groupby("Invoice")["TotalPrice"].sum().mean()
    total_countries = df["Country"].nunique()

    kpis = [
        ("Total Revenue",    f"£{total_revenue:,.0f}",   "💰", ACCENT),
        ("Total Orders",     f"{total_orders:,}",         "🧾", ACCENT2),
        ("Customers",        f"{total_customers:,}",      "👤", ACCENT3),
        ("Products",         f"{total_products:,}",       "📦", "#f96060"),
        ("Avg Order Value",  f"£{avg_order_value:,.2f}",  "🛒", "#56c9e0"),
        ("Countries",        f"{total_countries}",        "🌍", "#b06bfc"),
    ]

    cols = st.columns(6)
    for col, (label, value, icon, color) in zip(cols, kpis):
        with col:
            st.markdown(f"""
                <div style="background:{CARD}; border:1px solid {BORDER}; border-radius:14px;
                            padding:1.1rem 1rem; border-top:3px solid {color};">
                    <div style="font-size:1.1rem; margin-bottom:6px;">{icon}</div>
                    <div style="font-size:1.35rem; font-weight:700; color:{TEXT};
                                letter-spacing:-0.02em; line-height:1.1;">{value}</div>
                    <div style="font-size:0.7rem; color:{MUTED}; font-weight:600;
                                letter-spacing:0.06em; text-transform:uppercase;
                                margin-top:4px;">{label}</div>
                </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CHART 1 — Monthly Revenue Trend
# ─────────────────────────────────────────────
def chart_monthly_trend(df):
    monthly = (
        df.groupby(["Year", "Month", "Month_Name"])["TotalPrice"]
        .sum().reset_index().sort_values(["Year", "Month"])
    )
    monthly["Period"] = monthly["Month_Name"] + " " + monthly["Year"].astype(str)

    fig = px.area(
        monthly, x="Period", y="TotalPrice",
        title="Monthly Revenue Trend",
        labels={"TotalPrice": "Revenue (£)", "Period": ""},
        color_discrete_sequence=[ACCENT]
    )
    fig.update_traces(fillcolor=f"rgba(108,99,255,0.12)", line_width=2)
    return chart_layout(fig, height=300)


# ─────────────────────────────────────────────
#  CHART 2 — Top N Products
# ─────────────────────────────────────────────
def chart_top_products(df, top_n):
    top = (
        df.groupby("Description")["Quantity"]
        .sum().sort_values(ascending=False).head(top_n).reset_index()
    )
    fig = px.bar(
        top, x="Quantity", y="Description", orientation="h",
        title=f"Top {top_n} Best Selling Products",
        labels={"Quantity": "Units Sold", "Description": ""},
        color_discrete_sequence=[ACCENT]
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"},
                      showlegend=False, coloraxis_showscale=False)
    return chart_layout(fig, height=360)


# ─────────────────────────────────────────────
#  CHART 3 — Revenue by Country
# ─────────────────────────────────────────────
def chart_by_country(df):
    intl = df[df["Country"] != "United Kingdom"]
    by_country = (
        intl.groupby("Country")["TotalPrice"]
        .sum().sort_values(ascending=False).head(10).reset_index()
    )
    fig = px.bar(
        by_country, x="Country", y="TotalPrice",
        title="Top 10 International Markets",
        labels={"TotalPrice": "Revenue (£)", "Country": ""},
        color_discrete_sequence=[ACCENT2]
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return chart_layout(fig, height=360)


# ─────────────────────────────────────────────
#  CHART 4 — Sales by Day of Week
# ─────────────────────────────────────────────
def chart_day_of_week(df):
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_sales = (
        df.groupby("Day_of_Week")["TotalPrice"]
        .sum().reindex(day_order).reset_index()
    )
    fig = px.bar(
        day_sales, x="Day_of_Week", y="TotalPrice",
        title="Revenue by Day of Week",
        labels={"TotalPrice": "Revenue (£)", "Day_of_Week": ""},
        color_discrete_sequence=[ACCENT3]
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return chart_layout(fig, height=300)


# ─────────────────────────────────────────────
#  CHART 5 — Sales by Hour
# ─────────────────────────────────────────────
def chart_by_hour(df):
    hourly = df.groupby("Hour")["TotalPrice"].sum().reset_index()
    fig = px.line(
        hourly, x="Hour", y="TotalPrice",
        title="Revenue by Hour of Day",
        labels={"TotalPrice": "Revenue (£)", "Hour": "Hour"},
        markers=True, color_discrete_sequence=["#56c9e0"]
    )
    return chart_layout(fig, height=300)


# ─────────────────────────────────────────────
#  CHART 6 — Top Customers
# ─────────────────────────────────────────────
def chart_top_customers(df):
    top_c = (
        df.groupby("Customer ID")["TotalPrice"]
        .sum().sort_values(ascending=False).head(10).reset_index()
    )
    fig = px.bar(
        top_c, x="Customer ID", y="TotalPrice",
        title="Top 10 Most Valuable Customers",
        labels={"TotalPrice": "Total Spend (£)", "Customer ID": "Customer ID"},
        color_discrete_sequence=["#b06bfc"]
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return chart_layout(fig, height=300)


# ─────────────────────────────────────────────
#  INSIGHTS
# ─────────────────────────────────────────────
def show_insights(df):
    best_month   = df.groupby("Month_Name")["TotalPrice"].sum().idxmax()
    best_day     = df.groupby("Day_of_Week")["TotalPrice"].sum().idxmax()
    best_product = df.groupby("Description")["Quantity"].sum().idxmax()

    intl_df = df[df["Country"] != "United Kingdom"]
    best_intl = (
        intl_df.groupby("Country")["TotalPrice"].sum().idxmax()
        if not intl_df.empty else "N/A"
    )
    repeat_rate = round(
        (df[df.duplicated(subset="Customer ID", keep=False)]["Customer ID"].nunique()
         / df["Customer ID"].nunique()) * 100, 1
    )

    insights = [
        ("Peak Month",          best_month,          "Plan stock & staffing for this period",              ACCENT2,  "📅"),
        ("Best Selling Product", best_product[:40]+"…","Never let this go out of stock",                   ACCENT,   "📦"),
        ("Top Intl Market",     best_intl,            "Consider a local distribution partner",             ACCENT3,  "🌍"),
        ("Busiest Day",         best_day,             "Max staff, avoid maintenance windows",               "#56c9e0","📆"),
        ("Repeat Customer Rate",f"{repeat_rate}%",    "Customers who ordered more than once",              "#b06bfc","🔁"),
        ("Cancellations",       "Flagged in data",    "Investigate top cancelled products",                 "#f96060","🚫"),
    ]

    st.markdown(f'<div class="section-heading">Key Insights</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (title, value, note, color, icon) in enumerate(insights):
        with cols[i % 3]:
            st.markdown(f"""
                <div style="background:{CARD}; border:1px solid {BORDER}; border-radius:12px;
                            padding:1rem 1.1rem; margin-bottom:0.8rem; border-left:3px solid {color};">
                    <div style="font-size:0.68rem; color:{MUTED}; font-weight:700;
                                text-transform:uppercase; letter-spacing:0.1em; margin-bottom:6px;">
                        {icon} &nbsp;{title}
                    </div>
                    <div style="font-size:1rem; font-weight:700; color:{TEXT};
                                margin-bottom:4px; line-height:1.3;">{value}</div>
                    <div style="font-size:0.72rem; color:{MUTED};">{note}</div>
                </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  RFM CUSTOMER SEGMENTATION
# ─────────────────────────────────────────────
def show_rfm(df):
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = (
        df.groupby("Customer ID")
        .agg(
            Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
            Frequency=("Invoice", "nunique"),
            Monetary=("TotalPrice", "sum"),
        )
        .reset_index()
    )
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"),  5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    def segment(row):
        r, f = row["R_Score"], row["F_Score"]
        if r >= 4 and f >= 4:   return "Champions"
        elif r >= 3 and f >= 3: return "Loyal Customers"
        elif r >= 4 and f <= 2: return "New Customers"
        elif r >= 3 and f <= 2: return "Potential Loyalists"
        elif r <= 2 and f >= 3: return "At Risk"
        elif r == 1 and f >= 3: return "Lost Champions"
        else:                   return "Need Attention"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    segment_colors = {
        "Champions":           ACCENT,
        "Loyal Customers":     ACCENT2,
        "New Customers":       ACCENT3,
        "Potential Loyalists": "#56c9e0",
        "At Risk":             "#f96060",
        "Lost Champions":      "#b06bfc",
        "Need Attention":      "#f9d03f",
    }

    # ── Segment mini-cards ──
    seg_counts = rfm["Segment"].value_counts()
    st.markdown(f'<div class="section-heading">Customer Segments</div>', unsafe_allow_html=True)
    seg_cols = st.columns(len(seg_counts))
    for col, (seg, count) in zip(seg_cols, seg_counts.items()):
        pct   = round(count / len(rfm) * 100, 1)
        color = segment_colors.get(seg, ACCENT)
        with col:
            st.markdown(f"""
                <div style="background:{CARD}; border:1px solid {BORDER}; border-radius:12px;
                            padding:0.9rem 0.8rem; text-align:center; border-top:3px solid {color};
                            margin-bottom:0.8rem;">
                    <div style="font-size:1.2rem; font-weight:700; color:{TEXT};">{count:,}</div>
                    <div style="font-size:0.62rem; color:{MUTED}; font-weight:700;
                                text-transform:uppercase; letter-spacing:0.07em;
                                margin-top:2px;">{seg}</div>
                    <div style="font-size:0.7rem; color:{color}; margin-top:2px;">{pct}%</div>
                </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_scatter = px.scatter(
            rfm, x="Recency", y="Monetary", size="Frequency",
            color="Segment", color_discrete_map=segment_colors,
            title="Customer Map · Recency vs Monetary",
            labels={"Recency": "Days Since Last Purchase", "Monetary": "Total Spend (£)"},
            hover_data={"Customer ID": True, "Frequency": True, "RFM_Score": True},
            size_max=28,
        )
        fig_scatter.update_layout(legend=dict(font=dict(color=TEXT, size=11)))
        card(chart_layout(fig_scatter, height=360))

    with col2:
        seg_summary = (
            rfm.groupby("Segment")
            .agg(Customers=("Customer ID", "count"), Avg_Spend=("Monetary", "mean"))
            .reset_index().sort_values("Avg_Spend", ascending=False)
        )
        fig_bar = px.bar(
            seg_summary, x="Segment", y="Avg_Spend",
            title="Avg Spend by Segment",
            labels={"Avg_Spend": "Avg Total Spend (£)", "Segment": ""},
            color="Segment", color_discrete_map=segment_colors,
        )
        fig_bar.update_layout(showlegend=False, xaxis_tickangle=-20)
        card(chart_layout(fig_bar, height=360))

    action_map = {
        "Champions":           "Reward them — referral programmes, early access",
        "Loyal Customers":     "Upsell higher-value products; ask for reviews",
        "New Customers":       "Onboarding emails; highlight bestsellers",
        "Potential Loyalists": "Membership or loyalty scheme offer",
        "At Risk":             "Win-back campaign with a personalised discount",
        "Lost Champions":      "Aggressive re-engagement; survey why they left",
        "Need Attention":      "Send re-activation offer before they churn fully",
    }
    seg_summary["Recommended Action"] = seg_summary["Segment"].map(action_map)
    seg_summary["Avg_Spend"] = seg_summary["Avg_Spend"].map("£{:,.0f}".format)
    seg_summary = seg_summary.rename(columns={"Customers": "# Customers", "Avg_Spend": "Avg Spend"})

    st.markdown(f'<div class="section-heading" style="margin-top:0.5rem;">Segment Action Plan</div>',
                unsafe_allow_html=True)
    st.dataframe(
        seg_summary[["Segment", "# Customers", "Avg Spend", "Recommended Action"]],
        use_container_width=True, hide_index=True
    )


# ─────────────────────────────────────────────
#  RAW DATA EXPLORER
# ─────────────────────────────────────────────
def show_raw_data(df):
    with st.expander("Explore Raw Data"):
        st.markdown(f"<span style='color:{MUTED}; font-size:0.8rem;'>Showing "
                    f"<b style='color:{TEXT};'>{len(df):,}</b> rows after cleaning</span>",
                    unsafe_allow_html=True)
        st.dataframe(
            df[["Invoice", "Description", "Quantity", "Price",
                "TotalPrice", "InvoiceDate", "Country", "Customer ID"]].head(500),
            use_container_width=True
        )
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Cleaned CSV", csv, "cleaned_retail_data.csv", "text/csv")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    with st.spinner("Loading data..."):
        df = load_data()

    selected_years, selected_countries, top_n = sidebar_filters(df)

    filtered_df = df[
        (df["Year"].isin(selected_years)) &
        (df["Country"].isin(selected_countries))
    ]

    # ── Page header ──
    country_chips = "".join(
        f'<span style="display:inline-block; background:{ACCENT}22; border:1px solid {ACCENT}55; '
        f'border-radius:5px; padding:2px 10px; margin:2px 4px 2px 0; font-size:0.75rem; '
        f'color:{TEXT}; font-weight:500;">{c}</span>'
        for c in selected_countries
    )
    st.markdown(f"""
        <div style="margin-bottom:1.6rem;">
            <h1 style="font-size:1.7rem; font-weight:800; color:{TEXT};
                       letter-spacing:-0.03em; margin:0 0 4px 0;">
                UK Retail Sales Dashboard
            </h1>
            <p style="color:{MUTED}; font-size:0.82rem; margin:0 0 8px 0;">
                {len(filtered_df):,} transactions &nbsp;·&nbsp;
                {', '.join(map(str, selected_years))}
            </p>
            <div style="margin-top:4px;">{country_chips}</div>
        </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    show_kpis(filtered_df)
    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Revenue trend (full width) ──
    st.markdown(f'<div class="section-heading">Revenue Overview</div>', unsafe_allow_html=True)
    card(chart_monthly_trend(filtered_df))

    # ── Row: Products + Countries ──
    st.markdown(f'<div class="section-heading">Sales Breakdown</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: card(chart_top_products(filtered_df, top_n))
    with col2: card(chart_by_country(df))

    # ── Row: Day + Hour ──
    st.markdown(f'<div class="section-heading">Timing Patterns</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3: card(chart_day_of_week(filtered_df))
    with col4: card(chart_by_hour(filtered_df))

    # ── Top customers ──
    st.markdown(f'<div class="section-heading">Customer Value</div>', unsafe_allow_html=True)
    card(chart_top_customers(filtered_df))

    # ── Insights ──
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    show_insights(filtered_df)

    # ── RFM ──
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-heading">RFM Customer Segmentation</div>', unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-size:0.8rem; color:{MUTED}; margin:-0.4rem 0 1rem 0;'>"
        "Customers scored on Recency · Frequency · Monetary value</p>",
        unsafe_allow_html=True
    )
    show_rfm(filtered_df)

    # ── Raw data ──
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    show_raw_data(filtered_df)

    # ── Footer ──
    st.markdown(f"""
        <div style="text-align:center; color:{MUTED}; font-size:0.72rem;
                    margin-top:2rem; padding-top:1rem; border-top:1px solid {BORDER};">
            Built with Python · Streamlit · Plotly &nbsp;·&nbsp; UCI Online Retail II Dataset
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
