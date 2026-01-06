from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="cifar10_training_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ml", "training"],
) as dag:

    train_model = KubernetesPodOperator(
        task_id="train_cifar10_model",
        name="cifar10-train-pod",
        namespace="airflow",
        image="cifar10-train:1.0",
        cmds=["python"],
        arguments=["train.py"],
        get_logs=True,
        is_delete_operator_pod=True,
    )
