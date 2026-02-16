import pandas as pd
from openelectricity import OEClient
from openelectricity.types import MarketMetric
from datetime import datetime, timedelta

# Electricity pricing extraction for market price, timestamp, demand
# Initialize OpenElectricity client
client = OEClient()

start_time = datetime.now() - timedelta(days=1)  # Yesterday
end_time = datetime.now()  # Now

#API request
response = client.get_market(
    network_code = "NEM",
    network_region = "VIC1",
    metrics = [MarketMetric.PRICE, MarketMetric.DEMAND],
    interval = "1h",
)

#print(response.model_dump_json(indent=2))
df = response.to_pandas()

# 1. Ensure timestamp is actual datetime
df['interval'] = pd.to_datetime(df['interval'])

# 2. Collapse the NaNs by grouping by timestamp
# This takes the 'first' non-NaN value it finds for each hour
df_aligned = df.groupby('interval').first().reset_index()

# 3. Handle the Temperature Join
# (Now you can join your weather data here)
print(df_aligned)