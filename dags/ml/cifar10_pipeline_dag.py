from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    "owner": "ml-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=1),
}

with DAG(
    dag_id="cifar10_pipeline_training",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["ml", "cifar10", "etl"],
) as dag:

    from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
    from airflow.models import Variable
    from kubernetes.client import V1ResourceRequirements

    IMAGE = Variable.get(
        "cifar10_pipeline_image",
        default_var="ukesh01/cifar10-train:1.0"
    )

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
        container_resources=V1ResourceRequirements(
            requests={"cpu": "250m", "memory": "512Mi"},
            limits={"cpu": "500m", "memory": "1Gi"},
        ),
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
        container_resources=V1ResourceRequirements(
            requests={"cpu": "250m", "memory": "512Mi"},
            limits={"cpu": "500m", "memory": "1Gi"},
        ),
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
        container_resources=V1ResourceRequirements(
            requests={"cpu": "250m", "memory": "512Mi"},
            limits={"cpu": "500m", "memory": "1Gi"},
        ),
    )

    extract_data >> transform_data >> load_data
