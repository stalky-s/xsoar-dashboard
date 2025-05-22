import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# --- App Title ---
st.set_page_config(page_title="Security Dashboard", layout="centered")
st.title("XSOAR Dashboard SOC")

# --- Upload Excel File ---
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    DATE_COLUMN = "timestamp"
    RULE_COLUMN = "rulename"

    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
    df = df.dropna(subset=[RULE_COLUMN])

    today = pd.Timestamp.today().normalize()
    last_7_days = today - timedelta(days=7)

    df_today = df[df[DATE_COLUMN] >= today]
    df_week = df[df[DATE_COLUMN] >= last_7_days]

    def get_rule_counts(data, label):
        counts = data[RULE_COLUMN].value_counts().reset_index()
        counts.columns = ["Rule Name", "Count"]
        counts["Period"] = label
        return counts

    counts_today = get_rule_counts(df_today, "Today")
    counts_week = get_rule_counts(df_week, "Last 7 Days")
    summary_df = pd.concat([counts_today, counts_week])

    st.subheader("📋 Rule Trigger Summary")
    st.dataframe(summary_df, use_container_width=True)

    # --- Pie Charts ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rule Distribution Today")
        fig1, ax1 = plt.subplots()
        ax1.pie(counts_today["Count"], labels=counts_today["Rule Name"], autopct='%1.1f%%', startangle=140)
        ax1.axis("equal")
        st.pyplot(fig1)

    with col2:
        st.subheader("Last 7 Days")
        fig2, ax2 = plt.subplots()
        # Apply font size change using textprops
        ax2.pie(
            counts_week["Count"],
            labels=counts_week["Rule Name"],
            autopct='%1.1f%%',
            startangle=140,
            textprops={'fontsize': 12}  # 👈 change this number to adjust size
        )
        
        ax2.axis("equal")
        st.pyplot(fig2)

    # --- Line Plot ---
    st.subheader("Rule Triggers Over the Last 7 Days")
    df_week["date"] = df_week[DATE_COLUMN].dt.date
    trend = df_week.groupby(["date", RULE_COLUMN]).size().unstack(fill_value=0)

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    trend.plot(ax=ax3, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.title("Rule Triggers per Day")
    plt.tight_layout()
    st.pyplot(fig3)

else:
    st.info("Please upload a valid `.xlsx` file to begin.")
