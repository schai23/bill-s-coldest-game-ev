from __future__ import annotations

import requests
import pandas as pd
from datetime import date
from typing import Union

# Approx Highmark Stadium (Orchard Park, New York) coordinates from Google Maps 
# and https://www.latlong.net/place/highmark-stadium-ny-usa-31870.html  
STADIUM_LAT = 42.773773
STADIUM_LONG = -78.787460

# Open-Meteo histoircal weather API base URL
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

def fetch_daily_min_temps(
        start_date: Union[str, date],
        end_date: Union[str, date],
        timezone: str = "America/New_York",
) -> pd.DataFrame: 
    """
    Fetch daily minimum temperatures at Highmark Stadium between 
    start_date and end_date (inclusive) using Open-Meteo historical weather API

    Returns a DataFrame with columns: ["date", "min_temp_c"]
    """

    if isinstance(start_date, date):
        start_str = start_date.isoformat()
    else:
        start_str = str(start_date)

    if isinstance(end_date, date):
        end_str = end_date.isoformat()
    else:
        end_str = str(end_date)

    params = {
        "latitude": STADIUM_LAT,
        "longitude": STADIUM_LONG,
        "start_date": start_str,
        "end_date": end_str,
        "daily": "temperature_2m_min",
        "timezone": timezone,
    }

    resp = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    daily = data.get("daily", {})
    times = daily.get("time", [])
    temps = daily.get("temperature_2m_min", [])

    if not times or not temps:
        raise ValueError("No daily data returned from Open-Meteo")
    
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(times),
            "min_temp_c": temps,
        }
    )

    df["date"] = df["date"].dt.date

    return df