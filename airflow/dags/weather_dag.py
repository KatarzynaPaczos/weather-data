from dotenv import load_dotenv
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.models import Variable
from plugins.utils import  fetch_weather_data_for_locations,upload_to_s3


load_dotenv()
API_WEATHER = os.getenv("API_WEATHER")
S3_BUCKET = 'weather-based-on-lon-lat-bucket'
S3_KEY_PREFIX = 'raw/openweather'



locations = [
 {"lat": "54.6778816", "lon": "-5.9249199"},
 {"lat": "52.6362", "lon": "-1.1331969"},
 {"lat": "51.456659", "lon": "-0.9696512"},
 {"lat": "54.1775283", "lon": "-6.337506"},
 {"lat": "51.4867", "lon": "0.2433"},
 {"lat": "53.4071991", "lon": "-2.99168"},
 {"lat": "53.3045372", "lon": "-1.1028469453936067"},
 ]


def task_fetch(**context):
    data = fetch_weather_data_for_locations(locations, API_WEATHER)
    context['ti'].xcom_push(key='weather_data', value=data)


def task_upload(**context):
    weather_data = context['ti'].xcom_pull(task_ids='fetch_weather', key='weather_data')
    S3_BUCKET = Variable.get("S3_BUCKET") # i set them up on Airflow UI
    S3_KEY_PREFIX = Variable.get("S3_KEY_PREFIX") # i set them up on Airflow UI
    exec_date = context['ds']
    s3_path = upload_to_s3(weather_data, S3_BUCKET, S3_KEY_PREFIX, exec_date)
    print(f"Uploaded: {s3_path}")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_to_s3_dag',
    default_args=default_args,
    description='Fetch weather data from OpenWeatherMap and store in S3',
    schedule='@daily',
    start_date=datetime(2025, 10, 3),
    catchup=False,
    tags=['weather', 'openweathermap', 's3'],
) as dag:

    fetch_weather = PythonOperator(
        task_id='fetch_weather',
        python_callable=task_fetch
    )

    upload_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=task_upload
    )

    fetch_weather >> upload_s3
    