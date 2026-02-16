import pandas as pd
import pytz
from openelectricity import OEClient
from openelectricity.types import MarketMetric
from datetime import datetime, timedelta


def getMarketPrices():
    try:
        with OEClient() as client:
            end_time = datetime.now(pytz.utc)
            start_time = end_time - timedelta(hours=48)

            # 2. REMOVE MICROSECONDS
            # This keeps them as datetime objects but sets .886090 to .000000
            start_time = start_time.replace(microsecond=0)
            end_time = end_time.replace(microsecond=0)

            response = client.get_market(
                network_code="NEM",
                network_region="VIC1",
                metrics=[MarketMetric.PRICE, MarketMetric.DEMAND],
                interval="1h",
                date_start=start_time,
                date_end=end_time
            )

            df = response.to_pandas()

            # 1. Handle MultiIndex columns (Price/Demand)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0].name.lower() if hasattr(col[0], 'name') else str(col[0]).lower() 
                             for col in df.columns]

            df = df.reset_index()

            # 2. THE TIMEZONE FIX
            # Force to UTC first, then convert to Melbourne (+11), then strip TZ
            df['interval'] = pd.to_datetime(df['interval'])
            if df['interval'].dt.tz is None:
                df['interval'] = df['interval'].dt.tz_localize('UTC')
            
            df['interval'] = df['interval'].dt.tz_convert('Australia/Melbourne').dt.tz_localize(None)

            # 3. Align "Hour Ending" to "Hour Starting"
            # This makes 10:00 PM Price align with 10:00 PM Temperature
            df['interval'] = df['interval'] - pd.Timedelta(hours=1)

            # 4. Filter to the actual last 24 hours in Melbourne time
            melb_now = datetime.now(pytz.timezone('Australia/Melbourne')).replace(tzinfo=None)
            cutoff = melb_now - timedelta(hours=24)
            
            # Keep only rows that are not in the future and within the last 24h
            df = df[(df['interval'] <= melb_now) & (df['interval'] >= cutoff)]

            # Clean up duplicates if any
            df_aligned = df.groupby('interval').first().reset_index()

            return df_aligned
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    df = getMarketPrices()
    print(df)
    
