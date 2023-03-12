# Seb Week 2 Submission

## Step 1: Setup

- Watched all [videos](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_2_workflow_orchestration)
- Spotted this [summary](https://github.com/padilha/de-zoomcamp/tree/master/week2) and 
- Downloaded this [code](https://github.com/discdiver/prefect-zoomcamp)
- Pip3 installed week2 requirements.txt

### Notes on Videos

1. Data Lake: Overview differences Data Lake <> Data Warehouse; ETL <> ELT
2. Workflow Orchestration: tool to visualize data flows, execute them remotely, handle faults (retries), logging (log_prints=True) integrate with external services etc.
3. Prefect: Rewriting of ingest_data.py and adding @flow and @task decorates to track them in Prect Orion UI. Introduction of 'Prefect Blocks' to store SQLAlchemyConnector creds. 
4. ETL witH GCP and Prefect (file [ETL_WEB_TO_GCS](https://github.com/padilha/de-zoomcamp/blob/master/week2/etl_web_to_gcs.py)): saving data locally and uploading it to GCP!

## Step 2: Addressing Homework

### Question 1. Load January 2020 data

Using the `etl_web_to_gcs.py` flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

#### Solution

- 447,770 <<<<<<<<<<
- 766,792
- 299,234
- 822,132

#### Edits in Script

- Edit script and link. See that pick up and dropoff are starting with l.
- 'Unable to find block document named zoom-gcs for block type gcs-bucket': I linked the solution in the FAQ Google Doc.

#### Bash result

```bash
My logs: seb@private 02_gcp % python3 etl_web_to_gcs.py
11:50:07.693 | INFO    | prefect.engine - Created flow run 'precious-salamander' for flow 'etl-web-to-gcs'
11:50:07.763 | INFO    | Flow run 'precious-salamander' - Created task run 'fetch-b4598a4a-0' for task 'fetch'
11:50:07.763 | INFO    | Flow run 'precious-salamander' - Executing 'fetch-b4598a4a-0' immediately...
/Users/seb/Coding/DEZ/week_2_workflow_orchestration/flows/02_gcp/etl_web_to_gcs.py:14: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(dataset_url)
11:50:08.975 | INFO    | Task run 'fetch-b4598a4a-0' - Finished in state Completed()
11:50:08.986 | INFO    | Flow run 'precious-salamander' - Created task run 'clean-b9fd7e03-0' for task 'clean'
11:50:08.986 | INFO    | Flow run 'precious-salamander' - Executing 'clean-b9fd7e03-0' immediately...
11:50:09.104 | INFO    | Task run 'clean-b9fd7e03-0' -    VendorID lpep_pickup_datetime lpep_dropoff_datetime store_and_fwd_flag  ...  total_amount  payment_type  trip_type  congestion_surcharge
0       2.0  2019-12-18 15:52:30   2019-12-18 15:54:39                  N  ...          4.81           1.0        1.0                   0.0
1       2.0  2020-01-01 00:45:58   2020-01-01 00:56:39                  N  ...         24.36           1.0        2.0                   0.0

[2 rows x 20 columns]
11:50:09.105 | INFO    | Task run 'clean-b9fd7e03-0' - columns: VendorID                        float64
lpep_pickup_datetime     datetime64[ns]
lpep_dropoff_datetime    datetime64[ns]
store_and_fwd_flag               object
RatecodeID                      float64
PULocationID                      int64
DOLocationID                      int64
passenger_count                 float64
trip_distance                   float64
fare_amount                     float64
extra                           float64
mta_tax                         float64
tip_amount                      float64
tolls_amount                    float64
ehail_fee                       float64
improvement_surcharge           float64
total_amount                    float64
payment_type                    float64
trip_type                       float64
congestion_surcharge            float64
dtype: object
11:50:09.106 | INFO    | Task run 'clean-b9fd7e03-0' - rows: 447770
11:50:09.116 | INFO    | Task run 'clean-b9fd7e03-0' - Finished in state Completed()
11:50:09.128 | INFO    | Flow run 'precious-salamander' - Created task run 'write_local-f322d1be-0' for task 'write_local'
11:50:09.128 | INFO    | Flow run 'precious-salamander' - Executing 'write_local-f322d1be-0' immediately...
11:50:09.874 | INFO    | Task run 'write_local-f322d1be-0' - Finished in state Completed()
11:50:09.885 | INFO    | Flow run 'precious-salamander' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
11:50:09.885 | INFO    | Flow run 'precious-salamander' - Executing 'write_gcs-1145c921-0' immediately...
11:50:09.983 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'dtc_data_lake_aqueous-abbey-375520'.
11:50:11.193 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('data/green/green_tripdata_2020-01.parquet') to the bucket 'dtc_data_lake_aqueous-abbey-375520' path 'data/green/green_tripdata_2020-01.parquet'.
11:50:14.642 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
11:50:14.660 | INFO    | Flow run 'precious-salamander' - Finished in state Completed('All states completed.')
```

#### Used sript

```python
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    color = "green"  # "yellow"
    year = 2020  # 2021
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)
```

### Question 2. Scheduling with Cron

Cron is a common scheduling specification for workflows.

Using the flow in `etl_web_to_gcs.py`, create a deployment to run on the first of every month at 5am UTC. What’s the cron schedule for that?

#### Answer

- `0 5 1 * *` <<<<<0 5 1 * * >>>>>
- `0 0 5 1 *`
- `5 * 1 0 *`
- `* * 5 1 0`

### Question 3. Loading data to BigQuery

Using `etl_gcs_to_bq.py` as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. This new script should not fill or remove rows with missing values. (The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color.

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

#### Answer

- 14,851,920 <<<<<<<<< ~15M >>>>>>>>>
- 12,282,990
- 27,235,753
- 11,338,483

#### My edited code

```python
@flow(log_prints=True)
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    color = "yellow"
    year = 2019
    months = [2, 3]
    for month in months:
        path = extract_from_gcs(color, year, month)
        df = transform(path)
        write_bq(df)
```

#### Changelog

- [x] Logs decorator.
- [x] Multiple months.
- [x] color yellow, year 2019.

### Question 4. Github Storage Block

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. Prefect can look in the GitHub repo to find your flow code and read it. Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image.

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

#### Answer

- 88,019
- 192,297
- 88,605 <<< 88,605 >>>
- 190,225

#### My code edits

```python
from prefect.filesystems import GitHub
github_block = GitHub.load("dez")
```

### Question 5. Email or Slack notifications

Q5. It’s often helpful to be notified when something with your dataflow doesn’t work as planned. Choose one of the options below for creating email or slack notifications.

The hosted Prefect Cloud lets you avoid running your own server and has Automations that allow you to get notifications when certain events occur or don’t occur.

Create a free forever Prefect Cloud account at app.prefect.cloud and connect your workspace to it following the steps in the UI when you sign up.

Set up an Automation that will send yourself an email when a flow run completes. Run the deployment used in Q4 for the Green taxi data for April 2019. Check your email to see the notification.

Alternatively, use a Prefect Cloud Automation or a self-hosted Orion server Notification to get notifications in a Slack workspace via an incoming webhook.

Join my temporary Slack workspace with [this link](https://join.slack.com/t/temp-notify/shared_invite/zt-1odklt4wh-hH~b89HN8MjMrPGEaOlxIw). 400 people can use this link and it expires in 90 days.

In the Prefect Cloud UI create an [Automation](https://docs.prefect.io/ui/automations) or in the Prefect Orion UI create a [Notification](https://docs.prefect.io/ui/notifications/) to send a Slack message when a flow run enters a Completed state. Here is the Webhook URL to use: <https://hooks.slack.com/services/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>

Test the functionality.

Alternatively, you can grab the webhook URL from your own Slack workspace and Slack App that you create.

#### My webhook overview

![slack](img/seb_slack_webhook.png)

How many rows were processed by the script?

#### Answer

- `125,268`
- `377,922`
- `728,390`
- `514,392` <<< see line 4 below >>>

#### Bash outputs

```bash
15:07:02.845 | INFO    | prefect.engine - Created flow run 'hairy-tarsier' for flow 'etl-web-to-gcs'
15:07:02.917 | INFO    | Flow run 'hairy-tarsier' - Created task run 'fetch-b4598a4a-0' for task 'fetch'
15:07:02.918 | INFO    | Flow run 'hairy-tarsier' - Executing 'fetch-b4598a4a-0' immediately...
SD: Shape of df:  (514392, 20)
15:07:04.755 | INFO    | Task run 'fetch-b4598a4a-0' - Finished in state Completed()
15:07:04.770 | INFO    | Flow run 'hairy-tarsier' - Created task run 'clean-b9fd7e03-0' for task 'clean'
15:07:04.770 | INFO    | Flow run 'hairy-tarsier' - Executing 'clean-b9fd7e03-0' immediately...
15:07:04.912 | INFO    | Task run 'clean-b9fd7e03-0' - Finished in state Completed()
15:07:04.924 | INFO    | Flow run 'hairy-tarsier' - Created task run 'write_local-f322d1be-0' for task 'write_local'
15:07:04.924 | INFO    | Flow run 'hairy-tarsier' - Executing 'write_local-f322d1be-0' immediately...
15:07:05.927 | INFO    | Task run 'write_local-f322d1be-0' - Finished in state Completed()
15:07:05.937 | INFO    | Flow run 'hairy-tarsier' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
15:07:05.937 | INFO    | Flow run 'hairy-tarsier' - Executing 'write_gcs-1145c921-0' immediately...
15:07:06.032 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'dtc_data_lake_aqueous-abbey-375520'.
15:07:07.363 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('data/green/green_tripdata_2019-04.parquet') to the bucket 'dtc_data_lake_aqueous-abbey-375520' path 'data/green/green_tripdata_2019-04.parquet'.
15:07:12.297 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
15:07:12.316 | INFO    | Flow run 'hairy-tarsier' - Finished in state Completed('All states completed.')
```

### Question 6. Secrets

Prefect Secret blocks provide secure, encrypted storage in the database and obfuscation in the UI. Create a secret block in the UI that stores a fake 10-digit password to connect to a third-party service. Once you’ve created your block in the UI, how many characters are shown as asterisks (*) on the next page of the UI?

- 5
- 6
- 8
- 10

#### Screenshot

![secret](img/secretsasteriks.png)

#### Answer

<<<<<<<<<<All 10>>>>>>>>>>

This week, I helped with the following:

![help week 2](img/week_2_seb_help.png)