from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def start():
    print("task started")

def end():
    print("task ended")

with DAG(
    dag_id="two_task_dependency_dag",
    start_time=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)as dag:

    Start_task=PythonOperator(
        task_id="start_task",
        python_callable=start,
    )

    end_task=PythonOperator(
        task_id="end_task",
        python_callable=end,
    )

Start_task >> end_task