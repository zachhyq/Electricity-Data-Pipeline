
import pandas as pd
#import config
from sqlalchemy import create_engine, text



#url = config.DB_URL
url = "##"
engine = create_engine(url)


def load_data(df):
    df.to_sql('temp_electricity_prices', con=engine, if_exists='replace', index=False)


    upsert_query = text("""
        INSERT INTO electricity_prices (timestamp, region, demand, price, temperature)
        SELECT timestamp, region, demand, price, temperature FROM temp_electricity_prices
        ON DUPLICATE KEY UPDATE
            demand = VALUES(demand),
            price = VALUES(price),
            temperature = VALUES(temperature);
    """)

    with engine.begin() as conn:
        conn.execute(upsert_query)
        # 3. Clean up the temp table
        conn.execute(text("DROP TABLE temp_electricity_prices;"))

    print("✅ Data merged successfully (New rows added, existing rows updated).")
    


