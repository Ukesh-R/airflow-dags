from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def push():
    return "Data is pushing"

def pull(ti):
    data=ti.xcom_pull(task_ids="push_data")
    print(data)

with DAG(
    dag_id="Xcom_push_and_pull",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)as dag:
    
    push_data=PythonOperator(
        task_id="push_data",
        python_callable=push
    )

    pull_data=PythonOperator(
        task_id="pull_data",
        python_callable=pull
    )

    push_data >> pull_data