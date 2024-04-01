from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'rick_and_morty_etl',
    default_args=default_args,
    description='ETL process for Rick and Morty API data',
    # Set schedule_interval to None to only allow manual triggers
    schedule_interval=None,  
)

etl_task = BashOperator(
    task_id='run_etl',
    bash_command='python /opt/airflow/scripts/etl.py',
    dag=dag,
)
