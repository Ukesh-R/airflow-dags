from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.models import Variable

default_args = {
    "owner": "ml-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=1),
}

IMAGE = Variable.get(
    "cifar10_pipeline_image",
    default_var="ukesh01/cifar10-train:1.0"
)

with DAG(
    dag_id="cifar10_pipeline_training",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["ml", "cifar10", "etl"],
) as dag:

    extract_data = KubernetesPodOperator(
        task_id="extract_data",
        name="cifar10-extract",
        namespace="airflow",
        image=IMAGE,
        cmds=["python"],
        arguments=["/app/train.py"],
        is_delete_operator_pod=True,
        get_logs=True,
        labels={"stage": "extract"},
        resources={
            "request_cpu": "250m",
            "request_memory": "512Mi",
        },
    )

    transform_data = KubernetesPodOperator(
        task_id="transform_data",
        name="transform_data_pod",
        namespace="airflow",
        image=IMAGE,
        cmds=["python"],
        arguments=["/app/train.py"],
        is_delete_operator_pod=True,
        get_logs=True,
        labels={"stage": "transform"},
        resources={
            "request_cpu": "250m",
            "request_memory": "512Mi",
        },
    )

    load_data = KubernetesPodOperator(
        task_id="load_data",
        name="load_data_pod",
        namespace="airflow",
        image=IMAGE,
        cmds=["python"],
        arguments=["/app/train.py"],
        is_delete_operator_pod=True,
        get_logs=True,
        labels={"stage": "load"},
        resources={
            "request_cpu": "250m",
            "request_memory": "512Mi",
        },
    )

    extract_data >> transform_data >> load_data
