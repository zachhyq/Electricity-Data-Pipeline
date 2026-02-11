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

start_time = datetime.now() - timedelta(days=1)  # 7 days ago
end_time = datetime.now()  # Now

#API request for 24hr market data for NEM, VIC1 region, with 5 minute intervals
response = client.get_market(
    network_code = "NEM",
    metrics = [MarketMetric.PRICE],
    network_region = "VIC1",
    interval = "5m",
    date_end = end_time,
    date_start = start_time
)

print("Response Version:", response.version)
print("Total Records:", response.total_records)

sample_point = response.data[0].results[0].data[0]
pprint(sample_point.__dict__)


