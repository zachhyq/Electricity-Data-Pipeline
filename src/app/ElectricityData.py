#import config
import pandas as pd
from openelectricity import OEClient
from openelectricity.types import MarketMetric
from datetime import datetime, timedelta


NETWORK = "NEM"

def getMarketPrices(region):

    try:
        with OEClient() as client:

            start_time = datetime.now() - timedelta(days=1) - timedelta(hours=1)

            #Requesting Price and Demand data for specified region in past 24 hours
            response = client.get_market(
                network_code = NETWORK,
                network_region = region,
                metrics = [MarketMetric.PRICE, MarketMetric.DEMAND],
                interval="1h",
                date_start=start_time
            )

            df = response.to_pandas()
            #Convert to naive datetime object and then local timezone.
            df['interval'] = pd.to_datetime(df['interval']) - timedelta(hours=10)


            df = df.reset_index(drop=True)

            df_aligned = df.groupby('interval').first().reset_index()
            df_aligned.rename(columns={'interval': 'timestamp'}, inplace=True)

            return df_aligned
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    df = getMarketPrices()
    print(df)
    
