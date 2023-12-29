from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),  # Adjust the start date to your needs
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create a DAG instance
dag = DAG('run_book_spider',
          default_args=default_args,
          description='Run Scrapy Spider with BashOperator',
          schedule_interval=timedelta(days=1),  # Adjust the schedule to your needs
          catchup=False)  # Set to False if you don't want to perform catchup (backfilling past dates)

# Task to run the Scrapy spider
run_spider_task = BashOperator(
    task_id='run_scrapy_spider',
    # Ensure the command matches the path and name of your Scrapy project and spider
    bash_command='cd /root/projects/Scrapy-template/books && scrapy crawl book -o /root/output_files/book.csv',
    dag=dag)
