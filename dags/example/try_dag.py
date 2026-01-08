from airflow import DAG
from airflow.operators.python import PythonOperator

def say_hello():
    print("Hello")

with DAG(
     dag_id="print_Message",
     start_date=(2024, 1, 1),
     schedule=None,
     catchup=False,
)as dag:
    
    task_1=PythonOperator(
       Task_id="say hello",
       python_callable=say_hello,
)