from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {'owner': 'data-team', 'retries': 1, 'retry_delay': timedelta(minutes=5)}

with DAG('telecom_daily_pipeline', default_args=default_args, start_date=datetime(2026, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    generate = BashOperator(task_id='generate_cdr', bash_command='python 01_generate_cdr_data.py')
    process = BashOperator(task_id='spark_process', bash_command='python 02_spark_processing.py')
    load = BashOperator(task_id='load_warehouse', bash_command='python 03_load_snowflake.py')
    generate >> process >> load