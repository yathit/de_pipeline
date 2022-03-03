# Section 1: Data Pipelines
The objective of this section is to design and implement a solution to process a data file on a regular interval (e.g. daily). Assume that there are 2 data files `dataset1.csv` and `dataset2.csv`, design a solution to process these files, along with the scheduling component. The expected output of the processing task is a CSV file including a header containing the field names.

You can use common scheduling solutions such as `cron` or `airflow` to implement the scheduling component. You may assume that the data file will be available at 1am everyday. Please provide documentation (a markdown file will help) to explain your solution.

Processing tasks:
- Split the `name` field into `first_name`, and `last_name`
- Remove any zeros prepended to the `price` field
- Delete any rows which do not have a `name`
- Create a new field named `above_100`, which is `true` if the price is strictly greater than 100

# Solution

We will use [Apache Airflow](https://airflow.apache.org/) for this data processing task so that it is ready for production and future extension of the tasks. 

The initial data was downloaded into raw_zone and expected to have more data files everyday at 1 am.

## Setup

Setup Airflow

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
```

To start the service

    docker-compose up

The `data_pipeline` task will run every day 1 am and process additional files `raw_data` folder and produce `result.csv` file in `cleansed_zone` folder. 





