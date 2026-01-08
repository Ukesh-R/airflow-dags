from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
     dag_id="try_bash_dag",
     start_date=datetime(2024, 1, 1),
     schedule=None,
     catchup=False,
)as dag:
    
    bash_task=BashOperator(
         task_id="bash_task",
         bash_command="echo 'Hello from Bash' && date && ls",
    )