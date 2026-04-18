import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Page config
st.set_page_config(page_title="Marketing Dashboard", layout="wide")

# Title
st.title("📊 Marketing Campaign Funnel Analysis")
st.caption("Analyze performance, conversions and ROI")

# Sidebar
st.sidebar.header("🔍 Filters")

file = st.file_uploader("Upload Campaign Dataset", type=["csv"])

if file:
    df = pd.read_csv(file)
    df.fillna(0, inplace=True)

    # Metrics
    df["CTR"] = df["Clicks"] / df["Impressions"]
    df["Lead_Rate"] = df["Leads"] / df["Clicks"]
    df["Conversion_Rate"] = df["Conversions"] / df["Leads"]
    df.replace([float('inf'), -float('inf')], 0, inplace=True)

    # Sidebar filters
    channel_filter = st.sidebar.multiselect(
        "Channel",
        options=df["Channel_Used"].unique(),
        default=df["Channel_Used"].unique()
    )

    df = df[df["Channel_Used"].isin(channel_filter)]

    # ================= KPI SECTION =================
    st.subheader("📌 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Impressions", f"{df['Impressions'].sum():,}")
    col2.metric("Clicks", f"{df['Clicks'].sum():,}")
    col3.metric("Leads", f"{df['Leads'].sum():,}")
    col4.metric("Conversions", f"{df['Conversions'].sum():,}")

    # ================= DATA PREVIEW =================
    st.subheader("📂 Dataset Preview")
    st.dataframe(df.head())

    # ================= FUNNEL =================
    st.subheader("📉 Funnel Analysis")

    funnel_data = dict(
        stage=["Impressions", "Clicks", "Leads", "Conversions"],
        values=[
            df["Impressions"].sum(),
            df["Clicks"].sum(),
            df["Leads"].sum(),
            df["Conversions"].sum()
        ]
    )

    fig_funnel = px.funnel(funnel_data, x="values", y="stage",
                           title="Marketing Funnel")

    st.plotly_chart(fig_funnel, use_container_width=True)

    # ================= CHARTS =================
    st.subheader("📊 Performance Analysis")

    col1, col2 = st.columns(2)

    # Channel Revenue
    channel = df.groupby("Channel_Used")["Revenue"].sum().reset_index()
    fig1 = px.bar(channel, x="Channel_Used", y="Revenue",
                  title="Revenue by Channel", color="Channel_Used")

    # Conversion Rate
    conv = df.groupby("Channel_Used")["Conversion_Rate"].mean().reset_index()
    fig2 = px.bar(conv, x="Channel_Used", y="Conversion_Rate",
                  title="Conversion Rate by Channel", color="Channel_Used")

    with col1:
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    # ================= PIE =================
    st.subheader("🎯 Audience / Channel Share")

    fig3 = px.pie(channel, names="Channel_Used", values="Revenue",
                  title="Revenue Distribution")

    st.plotly_chart(fig3, use_container_width=True)

    # ================= INSIGHTS =================
    st.subheader("🧠 Insights & Recommendations")

    best_channel = channel.loc[channel["Revenue"].idxmax(), "Channel_Used"]
    worst_channel = channel.loc[channel["Revenue"].idxmin(), "Channel_Used"]

    total_clicks = df["Clicks"].sum()
    total_conversions = df["Conversions"].sum()

    conversion_rate = total_conversions / total_clicks if total_clicks != 0 else 0
    drop_off = 1 - conversion_rate

    st.success(f"✅ Best Performing Channel: {best_channel}")
    st.error(f"❌ Worst Performing Channel: {worst_channel}")
    st.warning(f"⚠️ Overall Drop-off Rate: {drop_off:.2%}")
    st.info("💡 Recommendation: Improve targeting and landing page to increase conversions")

# ================= STYLING =================
st.markdown("""
<style>
[data-testid="stMetric"] {
    background-color: #f5f7fa;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)
