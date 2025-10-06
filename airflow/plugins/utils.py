import requests
import json
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

def fetch_weather_data_for_locations(locations: list, api_key: str):
    results = []
    for loc in locations:
        lat = loc["lat"]
        lon = loc["lon"]
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            data["requested_lat"] = lat
            data["requested_lon"] = lon
            results.append(data)
        except Exception as e:
            print(f"Error fetching data for {lat}, {lon}: {e}")
    return results


def upload_to_s3(weather_data: list, bucket_name: str, key_prefix: str, exec_date: str):
    s3 = S3Hook()
    date_obj = datetime.strptime(exec_date, "%Y-%m-%d")
    s3_prefix = f"{key_prefix}/year={date_obj.year}/month={date_obj.month:02d}/day={date_obj.day:02d}"
    filename = f"{s3_prefix}/weather_{date_obj.strftime('%Y%m%d')}.ndjson"
    ndjson_data = "\n".join(json.dumps(record) for record in weather_data)
    s3.load_string(string_data=ndjson_data, key=filename, bucket_name=bucket_name, replace=True)
    return f"s3://{bucket_name}/{filename}"
