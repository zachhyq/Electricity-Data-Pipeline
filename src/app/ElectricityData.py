import pandas as pd
from openelectricity import OEClient
from openelectricity.types import MarketMetric
from datetime import datetime, timedelta


def getMarketPrices():
    try:
        with OEClient() as client:

            start_time = datetime.now() - timedelta(days=1) - timedelta(hours=1)


            response = client.get_market(
                network_code="NEM",
                network_region="VIC1",
                metrics=[MarketMetric.PRICE, MarketMetric.DEMAND],
                interval="1h",
                date_start=start_time
            )

            df = response.to_pandas()
            #Convert to naive datetime object and then local timezone.
            df['interval'] = pd.to_datetime(df['interval']) - timedelta(hours=10)
            


            # 1. Handle MultiIndex columns (Price/Demand)
            # if isinstance(df.columns, pd.MultiIndex):
            #     df.columns = [col[0].name.lower() if hasattr(col[0], 'name') else str(col[0]).lower() 
            #                  for col in df.columns]

            df = df.reset_index(drop=True)

            df_aligned = df.groupby('interval').first().reset_index()
            df_aligned.rename(columns={'interval': 'timestamp'}, inplace=True)

            return df_aligned
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    df = getMarketPrices()
    print(df)
    
