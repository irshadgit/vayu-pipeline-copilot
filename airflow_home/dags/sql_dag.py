from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import csv

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'student_database_pipeline',
    default_args=default_args,
    description='Create database, table, insert student data, and run custom query',
    schedule_interval=None,
    catchup=False,
    tags=['postgres', 'students'],
)

# Task 1: Create database if not exists
create_database = SQLExecuteQueryOperator(
    task_id='create_database',
    conn_id='postgres_students',
    sql="""
    SELECT 'CREATE DATABASE students_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'students_db');
    """,
    autocommit=True,
    doc_md="""
    ## Create Database Task
    
    This task creates a PostgreSQL database named `students_db` if it doesn't already exist.
    
    ### Purpose
    - Ensures the required database is available for subsequent operations
    - Uses conditional logic to avoid errors if database already exists
    
    ### SQL Logic
    The query uses PostgreSQL's `pg_database` system catalog to check if a database
    with the name 'students_db' already exists before attempting to create it.
    
    ### Parameters
    - **conn_id**: 'postgres_students' - Connection ID for PostgreSQL database
    - **autocommit**: True - Automatically commits the transaction
    
    ### Dependencies
    - None (first task in the pipeline)
    """,
    dag=dag,
)

# Task 2: Create table if not exists
create_table = SQLExecuteQueryOperator(
    task_id='create_table',
    conn_id='postgres_students',
    sql="""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INTEGER,
        grade VARCHAR(2),
        subject VARCHAR(50),
        score INTEGER,
        enrollment_date DATE
    );
    """,
    doc_md="""
    ## Create Table Task
    
    This task creates the `students` table with the required schema if it doesn't already exist.
    
    ### Purpose
    - Defines the table structure for storing student data
    - Uses IF NOT EXISTS to prevent errors on re-runs
    
    ### Table Schema
    - **student_id**: INTEGER PRIMARY KEY - Unique identifier for each student
    - **name**: VARCHAR(100) NOT NULL - Student's full name (required field)
    - **age**: INTEGER - Student's age
    - **grade**: VARCHAR(2) - Academic grade (e.g., 'A', 'B+')
    - **subject**: VARCHAR(50) - Subject name
    - **score**: INTEGER - Numeric score achieved
    - **enrollment_date**: DATE - Date when student enrolled
    
    ### Parameters
    - **conn_id**: 'postgres_students' - Connection ID for PostgreSQL database
    
    ### Dependencies
    - Depends on: create_database task
    """,
    dag=dag,
)

# Task 3: Read CSV and insert data
def read_and_insert_data(**context):
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    
    csv_file_path = context['dag'].folder + '/students_data.csv'
    
    hook = PostgresHook(postgres_conn_id='postgres_students')
    
    with hook.get_conn() as conn:
        with conn.cursor() as cursor:
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    cursor.execute("""
                        INSERT INTO students (student_id, name, age, grade, subject, score, enrollment_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (student_id) DO NOTHING;
                    """, (
                        row['student_id'],
                        row['name'],
                        row['age'],
                        row['grade'],
                        row['subject'],
                        row['score'],
                        row['enrollment_date']
                    ))
            conn.commit()

insert_data = PythonOperator(
    task_id='insert_student_data',
    python_callable=read_and_insert_data,
    doc_md="""
    ## Insert Student Data Task
    
    This task reads student data from a CSV file and inserts it into the students table.
    
    ### Purpose
    - Loads student data from external CSV file
    - Inserts data into the PostgreSQL students table
    - Uses ON CONFLICT to handle duplicate records gracefully
    
    ### Process Flow
    1. Opens the CSV file (students.csv) from the local filesystem
    2. Reads data using Python's csv.DictReader
    3. For each row, executes an INSERT statement with ON CONFLICT handling
    4. Commits the transaction to persist data
    
    ### Data Handling
    - **CSV Format**: Expected columns: student_id, name, age, grade, subject, score, enrollment_date
    - **Conflict Resolution**: Uses ON CONFLICT (student_id) DO NOTHING to skip duplicates
    - **Transaction Management**: Manually commits the connection after all inserts
    
    ### Error Handling
    - Gracefully handles duplicate student_id values
    - Closes database connections properly in all scenarios
    
    ### Parameters
    - **python_callable**: read_and_insert_data function
    - **CSV File Path**: './students.csv' (configurable)
    
    ### Dependencies
    - Depends on: create_table task
    """,
    dag=dag,
)

# Task 4: Run custom SQL query from Airflow Variable
run_custom_query = SQLExecuteQueryOperator(
    task_id='run_custom_query',
    conn_id='postgres_students',
    sql="{{ var.value.student_query }}",
    doc_md="""
    ## Run Custom Query Task
    
    This task executes a custom SQL query stored in an Airflow Variable.
    
    ### Purpose
    - Provides flexibility to run different SQL queries without code changes
    - Allows dynamic query execution based on business requirements
    - Demonstrates Airflow Variable usage for configuration
    
    ### Configuration
    - **Variable Name**: 'student_query'
    - **Variable Access**: Uses Jinja templating {{ var.value.student_query }}
    - **Query Type**: Any valid SQL query that can be executed against the students table
    
    ### Example Queries
    ```sql
    -- Get top 10 students by score
    SELECT * FROM students ORDER BY score DESC LIMIT 10;
    
    -- Average score by grade
    SELECT grade, AVG(score) as avg_score FROM students GROUP BY grade;
    
    -- Students enrolled in the last 30 days
    SELECT * FROM students WHERE enrollment_date >= CURRENT_DATE - INTERVAL '30 days';
    ```
    
    ### Setup Requirements
    1. Create an Airflow Variable named 'student_query'
    2. Set the variable value to your desired SQL query
    3. Ensure the query is compatible with PostgreSQL syntax
    
    ### Parameters
    - **conn_id**: 'postgres_students' - Connection ID for PostgreSQL database
    - **sql**: Dynamic query from Airflow Variable
    
    ### Dependencies
    - Depends on: insert_student_data task
    """,
    dag=dag,
)

# Set task dependencies
create_database >> create_table >> insert_data >> run_custom_query