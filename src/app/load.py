"""
Module holds the load_data function which upserts a dataframe into the electricity_prices table in MySQL.
Input dataframe should be preprocessed and have the same schema as the electricity_prices table (timestamp, region, demand, price, temperature).
"""

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text



def load_data(df):

    load_dotenv(".env.db")
    url = os.getenv("APP_DB_URL")
    engine = create_engine(url)


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

        conn.execute(text("DROP TABLE temp_electricity_prices;"))

    print("✅ Data merged successfully (New rows added, existing rows updated).")
    


