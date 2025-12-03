import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('weather_data.csv')

data = data.dropna(subset=['Temperature', 'Rainfall', 'Humidity'])
data['Date'] = pd.to_datetime(data['Date'])
data = data[['Date', 'Temperature', 'Rainfall', 'Humidity']]

monthly_stats = data.resample('M', on='Date').agg({
    'Temperature': ['mean', 'min', 'max', 'std'],
    'Rainfall': ['mean', 'min', 'max', 'std'],
    'Humidity': ['mean', 'min', 'max', 'std']
})
yearly_stats = data.resample('Y', on='Date').agg({
    'Temperature': ['mean', 'min', 'max', 'std'],
    'Rainfall': ['mean', 'min', 'max', 'std'],
    'Humidity': ['mean', 'min', 'max', 'std']
})

plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Temperature'])
plt.savefig('daily_temperature.png')
plt.close()

monthly_rainfall = data.resample('M', on='Date')['Rainfall'].sum()
plt.figure(figsize=(10, 5))
plt.bar(monthly_rainfall.index, monthly_rainfall.values)
plt.savefig('monthly_rainfall.png')
plt.close()

plt.figure(figsize=(8, 6))
plt.scatter(data['Temperature'], data['Humidity'])
plt.savefig('humidity_vs_temperature.png')
plt.close()

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(data['Date'], data['Temperature'], color='orange')
plt.subplot(2, 1, 2)
plt.bar(monthly_rainfall.index, monthly_rainfall.values, color='blue')
plt.tight_layout()
plt.savefig('combined_plot.png')
plt.close()

data['Month'] = data['Date'].dt.month
monthly_agg = data.groupby('Month').agg({
    'Temperature': ['mean', 'min', 'max'],
    'Rainfall': 'sum',
    'Humidity': 'mean'
})

data.to_csv('cleaned_weather_data.csv', index=False)
monthly_stats.to_csv('monthly_statistics.csv')
yearly_stats.to_csv('yearly_statistics.csv')
monthly_agg.to_csv('monthly_aggregation.csv')

report = f"""
Weather Data Analysis Report

1. Daily Temperature Trend: daily_temperature.png
2. Monthly Rainfall: monthly_rainfall.png
3. Humidity vs Temperature: humidity_vs_temperature.png
4. Combined Plot: combined_plot.png

Monthly Aggregated Statistics:
{monthly_agg.to_string()}

Insights:
- Temperature shows seasonal trends.
- Rainfall peaks in certain months indicating rainy season.
- Humidity generally follows temperature patterns.
"""
with open('weather_report.txt', 'w') as f:
    f.write(report)
