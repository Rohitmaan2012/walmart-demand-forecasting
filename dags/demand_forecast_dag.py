# dags/demand_forecast_dag.py
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="demand_forecast_daily",
    start_date=datetime(2025,10,1),
    schedule_interval="@daily",
    catchup=False,
    tags=["mlops","lakehouse","demo"]
) as dag:

    etl = BashOperator(
        task_id="etl",
        bash_command="export JAVA_HOME=/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home && source .venv/bin/activate && python scripts/etl_incremental.py",
        retries=2,
        retry_delay=60
    )

    train = BashOperator(
        task_id="train",
        bash_command="export JAVA_HOME=/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home && source .venv/bin/activate && MLFLOW_TRACKING_URI=file://$(pwd)/mlruns python scripts/train_gbt.py",
        retries=2,
        retry_delay=60
    )

    infer = BashOperator(
        task_id="batch_infer",
        bash_command="export JAVA_HOME=/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home && source .venv/bin/activate && MLFLOW_TRACKING_URI=file://$(pwd)/mlruns python scripts/batch_infer.py 7",
        retries=2,
        retry_delay=60
    )

    etl >> train >> infer
