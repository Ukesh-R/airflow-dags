from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import requests

def call_api():
    response= requests.get("https://dog.ceo/api/breeds/image/random",timeout=5)
    response.raise_for_status()
    print("API Call Successful")

with DAG(
     dag_id="Api_status_check",
     start_date=datetime(2024, 1, 1),
     schedule=None,
     catchup=False,
)as dag:
    
    Api_request_check=PythonOperator(
      task_id="Api_request_check",
      python_callable=call_api,
      retries=3,
      retry_delay=timedelta(minutes=2),
    )