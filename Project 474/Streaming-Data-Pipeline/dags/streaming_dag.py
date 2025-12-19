# dags/spark_streaming_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from spark_job.run_streaming import run_streaming

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG('spark_streaming_dag',
         default_args=default_args,
         schedule_interval='*/1 * * * *', # Run ทุกๆ 1 นาที
         catchup=False,
         max_active_runs=1, # ไม่ให้ run DAG ซ้ําถ้ามีตัวก่อนหน้ายัง running ไม่เสร็จ
         concurrency=1, # Task ตัวนี้ไม่ให้รันพร้อมกันหลาย instance
         tags=['streaming, spark, cassandra']
         ) as dag:

    streaming_task = PythonOperator(
        task_id='run_streaming',
        python_callable=run_streaming
    )

