import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Marketing Campaign Funnel Analysis")

file = st.file_uploader("Upload Campaign Dataset", type=["csv"])

if file:
    df = pd.read_csv(file)

    df.fillna(0, inplace=True)

    # Metrics
    df["CTR"] = df["Clicks"] / df["Impressions"]
    df["Lead_Rate"] = df["Leads"] / df["Clicks"]
    df["Conversion_Rate"] = df["Conversions"] / df["Leads"]
    df.replace([float('inf'), -float('inf')], 0, inplace=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Funnel totals
    funnel = df[["Impressions","Clicks","Leads","Conversions"]].sum()

    st.subheader("Funnel Overview")
    st.write(funnel)

    # Bar chart
    fig, ax = plt.subplots()
    ax.bar(funnel.index, funnel.values)
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # Channel performance
    st.subheader("Channel Performance")
    channel = df.groupby("Channel_Used")["Revenue"].sum()
    st.bar_chart(channel)

    # Insights
    st.subheader("Insights")

    best_channel = channel.idxmax()
    st.write(f"Best performing channel: {best_channel}")

    avg_ctr = df["CTR"].mean()
    st.write(f"Average CTR: {avg_ctr:.2f}")