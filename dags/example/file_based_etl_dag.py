from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def extract():
    with open("/data/test.txt", "w")as f:
        f.write("Hello Airflow")

def transform():
    with open("/data/test.txt","a")as f:
        f.write(" success")

def load():
    os.rename("/data/test.txt", "/data/final_data.txt")
    
with DAG(
     dag_id="ETL_load_data",
     start_date=datetime(2024, 1, 1),
     schedule=None,
     catchup=False,
)as dag:
    
    extract_data=PythonOperator(
        task_id="extract_data",
        python_callable=extract
    )
    transform_data=PythonOperator(
        task_id="transform_data",
        python_callable=transform
    )
    load_data=PythonOperator(
        task_id="load_data",
        python_callable=load
    )

    extract_data >> transform_data >> load_data
