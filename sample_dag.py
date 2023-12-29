# Importing necessary libraries
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define the Python function
def print_hello():
    print("Hello, World!")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate a DAG
dag = DAG('hello_world_dag',
          description='Simple tutorial DAG',
          schedule_interval=timedelta(days=1),  # This DAG is set to run daily
          start_date=datetime(2023, 8, 30),
          catchup=False,
          default_args=default_args)

# Set up a task using the PythonOperator
hello_task = PythonOperator(task_id='print_hello_world',
                            python_callable=print_hello,
                            dag=dag)

# Set the task order (in this case, only one task, so this is optional)
hello_task

