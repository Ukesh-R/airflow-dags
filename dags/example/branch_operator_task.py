from airflow import DAG
from airflow.operators.branch import BranchPythonOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def check_file():
    if os.path.exists("/tmp/data.txt"):
        return "process_task"
    return "skip_task"

def process():
    print("task is processing....")

def skip():
    print("skipping the process....")

with DAG(
    dag_id="verify_the_file",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)as dag:
    
    check_task=BranchPythonOperator(
        task_id="verify_the_process",
        python_callable=check_file
    )

    process_task=PythonOperator(
        task_id="process_task",
        python_callable=process
    )

    skip_task=PythonOperator(
        task_id="skip_task",
        python_callable=skip
    )