from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime

def variables_check():
    env=Variable.get("env_config", default_var="local")
    print(f"running in {env} environment")

with DAG(
    dag_id="airflow_variables",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
)as dag:
    
    PythonOperator(
        task_id="airflow_variables_check",
        python_callable=variables_check,
    )