from dotenv import load_dotenv
import os
import pandas as pd
from pprint import pprint
from openelectricity import OEClient
from openelectricity.types import MarketMetric
from datetime import datetime, timedelta

#Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENELECTRICITY_API_KEY")

if not API_KEY:
    raise ValueError("API Key missing in .env file.")
print("API Key loaded successfully.")

#Initialize OpenElectricity client
client = OEClient()

start_time = datetime.now() - timedelta(days=1)  # Yesterday
end_time = datetime.now()  # Now

#API request
response = client.get_market(
    network_code = "NEM",
    metrics = [MarketMetric.PRICE],
    network_region = "VIC1",
    interval = "1h",
    date_end = end_time,
    date_start = start_time
)

#print(response.model_dump_json(indent=2))

rows = []

# Step 1: Access the 'data' list
for network_block in response.data:
    metric_type = network_block.metric
    
    # Step 2: Access the 'results' list
    for result in network_block.results:
        # 'name' usually contains the region (e.g., 'price_VIC1')
        series_name = result.name
        
        # Step 3: Access the 'data' list of lists
        for point in result.data:
            # point.root is the [timestamp, value] list
            timestamp, value = point.root
            
            rows.append({
                "timestamp": timestamp,
                "label": series_name,
                "metric": metric_type,
                "value": value
            })

df = pd.DataFrame(rows)
df['timestamp'] = pd.to_datetime(df['timestamp'])

print(df.head())