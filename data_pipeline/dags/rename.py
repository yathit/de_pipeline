import os
import re
from datetime import datetime, timedelta

import pandas as pd
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

IN_PATH = 'raw_zone'
OUT_PATH = os.path.join('cleansed_zone', 'result.csv')


def process_name_price(datafile):
    filepaths = [f for f in os.listdir(IN_PATH) if f.endswith('.csv')]
    df = pd.concat(map(pd.read_csv, filepaths))

    in_shape = df.shape

    outdf = df.copy()
    # take last 2 space-delimited tokens as first and last name. assumes name field has at least 2 space-delimited tokens in string
    outdf['firstname'] = outdf['name'].apply(lambda x: re.split(' ', x)[-2])
    outdf['lastname'] = outdf['name'].apply(lambda x: re.split(' ', x)[-1])
    # pandas automatically reads numeric column, removing prepended 0s
    # remove rows with no name
    outdf = outdf.loc[outdf['name'] != '']
    # flag if price > 100
    outdf['above_100'] = outdf['price'].apply(lambda x: 'true' if x > 100 else 'false')

    outdf = outdf[['firstname', 'lastname', 'price', 'above_100']]
    # write to output file
    outdf.to_csv(OUT_PATH, index=False)

    outshape = outdf.shape

    # log diff in records between infile and outfile
    result = {
        'inshape': in_shape,
        'outshape': outshape
    }

    return result


with DAG(
        'data_pipeline',
        description='Rename, clean price and add above_100',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2022, 1, 1),
        catchup=False,
        tags=['test'],
        default_args={
            'depends_on_past': False,
            'email': ['airflow@example.com'],
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 0,
            'retry_delay': timedelta(minutes=5),
            'start_date': datetime(2022, 2, 26),
            # 'queue': 'bash_queue',
            # 'pool': 'backfill',
            # 'priority_weight': 10,
            # 'end_date': datetime(2016, 1, 1),
            # 'wait_for_downstream': False,
            # 'sla': timedelta(hours=2),
            # 'execution_timeout': timedelta(seconds=300),
            # 'on_failure_callback': some_function,
            # 'on_success_callback': some_other_function,
            # 'on_retry_callback': another_function,
            # 'sla_miss_callback': yet_another_function,
            # 'trigger_rule': 'all_success'
        },

) as dag:

    process_name_price_task = PythonOperator(
        # The task ID is what appears in the graph/tree view
        task_id="process_name_price",
        # Set this to TRUE or else we cannot access ti object
        provide_context=True,
        # This is like your main() method
        python_callable=process_name_price,
        dag=dag
    )

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t1 >> process_name_price_task



