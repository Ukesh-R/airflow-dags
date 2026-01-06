from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    dag_id="cifar10_training_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['ml', 'training'],
)as dag:

 train_model=DockerOperator(
    task_id="cifar10_model",
    image="cifar10-train:1.0",
    api_version="auto",
    auto_remove="success",
    command="python train.py",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge"
)