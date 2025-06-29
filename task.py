import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import os

zip_path =   "C:/Users/adras/Downloads/archive (1) task 2.zip"

extract_folder = "unemployment_data"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

for file in os.listdir(extract_folder):
    if file.endswith(".csv"):
        data_path = os.path.join(extract_folder, file)

df = pd.read_csv(data_path)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df.rename(columns={
    "estimated_unemployment_rate_(%)": "unemployment_rate",
    "estimated_labour_participation_rate_(%)": "labour_participation_rate"
}, inplace=True)

df['date'] = pd.to_datetime(df['date'], errors='coerce')

df.dropna(subset=['region', 'date', 'unemployment_rate'], inplace=True)

plt.figure(figsize=(14, 6))
avg_rate = df.groupby("date")["unemployment_rate"].mean()
plt.plot(avg_rate.index, avg_rate.values, marker='o', linestyle='-')
plt.title("📈 Average Unemployment Rate Over Time (India)")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

covid_df = df[(df['date'] >= '2020-01-01') & (df['date'] <= '2021-12-31')]
covid_avg = covid_df.groupby("date")["unemployment_rate"].mean()

plt.figure(figsize=(14, 6))
plt.plot(covid_avg.index, covid_avg.values, color='red', marker='x')
plt.title("📉 Unemployment Rate During COVID-19 (2020–2021)")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

df['month'] = df['date'].dt.month
monthly_avg = df.groupby("month")["unemployment_rate"].mean()

plt.figure(figsize=(10, 5))
sns.barplot(x=monthly_avg.index, y=monthly_avg.values, palette='coolwarm')
plt.title("📊 Average Unemployment Rate by Month")
plt.xlabel("Month (1=Jan, 12=Dec)")
plt.ylabel("Unemployment Rate (%)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 8))
sns.lineplot(data=df, x="date", y="unemployment_rate", hue="region", legend=False)
plt.title("🗺️ Unemployment Trend by Region (India)")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.tight_layout()
plt.show()
