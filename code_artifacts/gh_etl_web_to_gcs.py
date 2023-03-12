from random import randint
from pathlib import Path
import pandas as pd
import numpy as np
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df


@task()
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""

    # yellow taxi data
    # df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    # df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    # green taxi data
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    df["PULocationID"] = df.PULocationID.astype("Int64")
    df["DOLocationID"] = df.DOLocationID.astype("Int64")
    df['passenger_count'] = df['passenger_count'].astype('Int64')
    df['payment_type'] = df['payment_type'].astype('Int64')
    df['RatecodeID'] = df['RatecodeID'].astype('Int64')
    df['trip_type'] = df['trip_type'].astype('Int64')
    df['VendorID'] = df['VendorID'].astype('Int64')

    # fhv
    # df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    # df["Affi"] = df.PUlocationID.astype("Int64")
    # df["PUlocationID"] = df.PUlocationID.astype("Int64")
    # df["DOlocationID"] = df.DOlocationID.astype("Int64")
    # print(df.isnull().sum())
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    # get token from
    gcs_block = GcsBucket.load("zoomcamp-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""

    year = 2020

    for month in range(1, 13):

        # fhv
        # dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{month:02}.csv.gz"
        # dataset_file = f"data/fhv/fhv_tripdata_{year}-{month:02}"

        # yellow
        # dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month:02}.csv.gz"
        # dataset_file = f"data/yellow/yellow_tripdata_{year}-{month:02}"

        # green
        dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_{year}-{month:02}.csv.gz"
        dataset_file = f"data/green/green_tripdata_{year}-{month:02}"
        print(f'### Current Setup: {year}, {dataset_file} ###')
        df = fetch(dataset_url)
        df_clean = clean(df)
        print(df_clean.dtypes)
        path = write_local(df_clean, dataset_file)
        write_gcs(f"{dataset_file}.parquet")


if __name__ == "__main__":
    etl_web_to_gcs()
