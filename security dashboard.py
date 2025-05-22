# 📦 Imports
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from IPython.display import display, HTML

# 📁 Upload Excel File
from google.colab import files
uploaded = files.upload()  # Upload 'security_logs.xlsx'

# 📂 Load Excel
EXCEL_FILE = "security_logs.xlsx"
DATE_COLUMN = "timestamp"
RULE_COLUMN = "rulename"

df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
df = df.dropna(subset=[RULE_COLUMN])

# 📅 Date Filtering
today = pd.Timestamp.today().normalize()
last_7_days = today - timedelta(days=7)

df_today = df[df[DATE_COLUMN] >= today]
df_week = df[df[DATE_COLUMN] >= last_7_days]

# 📊 Summary Function
def rule_summary(data, label):
    counts = data[RULE_COLUMN].value_counts().reset_index()
    counts.columns = ['Rule Name', 'Count']
    counts['Period'] = label
    return counts

counts_today = rule_summary(df_today, "Today")
counts_week = rule_summary(df_week, "Last 7 Days")

# 🌐 Styled Header
display(HTML("<h1 style='color:#2c3e50;'>🔐 Security Rule Monitoring Dashboard</h1>"))

# 📋 Show Tables
display(HTML("<h2 style='color:#34495e;'>📅 Rule Triggers Today</h2>"))
display(counts_today)

display(HTML("<h2 style='color:#34495e;'>🗓️ Rule Triggers - Last 7 Days</h2>"))
display(counts_week)

# 📈 Line Plot for Trend
df_week['date'] = df_week[DATE_COLUMN].dt.date
daily_counts = df_week.groupby(['date', RULE_COLUMN]).size().unstack(fill_value=0)

plt.figure(figsize=(10, 5))
daily_counts.plot(marker='o', linewidth=2)
plt.title("📈 Daily Rule Triggers (Last 7 Days)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Trigger Count")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🥧 Pie Charts
def plot_pie(counts_df, title):
    plt.figure(figsize=(6, 6))
    plt.pie(counts_df['Count'], labels=counts_df['Rule Name'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(title, fontsize=13)
    plt.tight_layout()
    plt.show()

plot_pie(counts_today, "🥧 Rule Distribution Today")
plot_pie(counts_week, "🥧 Rule Distribution - Last 7 Days")
