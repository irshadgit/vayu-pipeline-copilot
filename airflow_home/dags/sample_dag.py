from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'sample_dag',
    default_args=default_args,
    description='A sample DAG with 3 tasks: EmptyOperator, BashOperator, and PythonOperator',
    schedule_interval=None,
    params={
        'first_number': 5,
        'second_number': 3,
    },
    catchup=False,
    tags=['sample', 'demo'],
)

def add_numbers(**context):
    """
    Simple function that adds two numbers from DAG params and prints the result.
    
    Args:
        context: Airflow context containing DAG run parameters
    
    Returns:
        int: Sum of the two numbers
    """
    # Get parameters from DAG run context with default values
    dag_run = context.get('dag_run')
    params = dag_run.conf if dag_run and dag_run.conf else {}
    
    a = params.get('first_number', 5)  # Default value: 5
    b = params.get('second_number', 3)  # Default value: 3
    
    result = a + b
    print(f"Adding {a} + {b} = {result}")
    print(f"Parameters used: first_number={a}, second_number={b}")
    return result

# Task 1: Empty Operator (Start task)
start_task = EmptyOperator(
    task_id='start_task',
    dag=dag,
)

# Task 2: Bash Operator with echo command
bash_task = BashOperator(
    task_id='bash_task',
    bash_command='echo "Hello World from Airflow!"',
    dag=dag,
)

# Task 3: Python Operator with simple addition function
python_task = PythonOperator(
    task_id='python_task',
    python_callable=add_numbers,
    dag=dag,
)

# Define task dependencies
start_task >> bash_task >> python_task
