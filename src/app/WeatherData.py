import requests
import pandas as pd
from datetime import datetime, timedelta

def get_temps():
    try:
        start_time = datetime.now() - timedelta(hours=24)
        end_time = datetime.now() - timedelta(hours=1)  # Get data up to the last full hour
        print(start_time, end_time)

        # Define the API endpoint and parameters
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": -37.8136,  # Melbourne latitude
            "longitude": 144.9631,  # Melbourne longitude
            "hourly": "temperature_2m",
            "start_hour": start_time.strftime("%Y-%m-%dT%H:00"),   
            "end_hour": end_time.strftime("%Y-%m-%dT%H:00"),
            "forecast_days": 0,
            "timezone": "Australia/Sydney"
        }

        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the JSON response
        data = response.json()
        hourly_data = data.get("hourly", {})
        temperatures = hourly_data.get("temperature_2m", [])
        timestamps = hourly_data.get("time", [])

        # Create a DataFrame from the temperatures and timestamps
        df_temps = pd.DataFrame({
            "timestamp": pd.to_datetime(timestamps),
            "temperature": temperatures
        })
        

        return df_temps

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching temperature data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
if __name__ == "__main__":
    df_temps = get_temps()
    print(df_temps)