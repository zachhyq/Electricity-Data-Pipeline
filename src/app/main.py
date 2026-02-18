import ElectricityData
import WeatherData
import pandas as pd


df_electricity = ElectricityData.getMarketPrices()
df_weather = WeatherData.get_temps()
df_merged = pd.merge(df_electricity, df_weather, on='timestamp', how='inner')
print(df_merged)
