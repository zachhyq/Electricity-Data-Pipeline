import ElectricityData
import WeatherData
import load
import pandas as pd

regions = ["VIC1", "NSW1", "QLD1", "SA1", "TAS1"]
coords = {"VIC1": {"latitude": -37.8136, "longitude": 144.9631},
          "NSW1": {"latitude": -33.8688, "longitude": 151.2093},
          "QLD1": {"latitude": -27.4698, "longitude": 153.0251},
          "SA1": {"latitude": -34.9285, "longitude": 138.6007},
          "TAS1": {"latitude": -42.8821, "longitude": 147.3272}
        }

# Collect all data into dataframe for loading. 
# (PK: timestamp + region, price, demand, temperature, region)
df_main = pd.DataFrame()
print("reached")
for region in regions:
    df_region_electricity = ElectricityData.getMarketPrices(region)
    df_region_weather = WeatherData.get_temps(coords[region])

    df_region_merged = pd.merge(df_region_electricity, df_region_weather, on='timestamp', how='inner')
    df_region_merged['region'] = region  # Add region column
    df_region_merged = df_region_merged[['timestamp', 'region', 'price', 'demand', 'temperature']]  # Reorder columns

    df_main = pd.concat([df_main, df_region_merged], ignore_index=True)

print(df_main)

load.load_data(df_main)
    