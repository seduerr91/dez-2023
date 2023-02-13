# Seb Week 3 Submission

## Step 1: Setup

- Watched all [videos](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_3_data_warehouse)
- Spotted this [summary](https://github.com/padilha/de-zoomcamp/tree/master/week3) and 
- Download 2019 data: ​https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv

## Step 2: Addressing Homework

### Question 1 What is the count for fhv vehicle records for year 2019?

- 65,623,481
- `43,244,696`
- 22,978,333
- 13,942,414

Before working on further exercises, I had to clean up the parquets first in my gh_etl_web_to_gcs.py script with:

```python
df["PUlocationID"] = df.PUlocationID.astype("Int64")
df["DOlocationID"] = df.DOlocationID.astype("Int64")
```

```sql
-- Ingestion External Table

CREATE OR REPLACE EXTERNAL TABLE `aqueous-abbey-375520.trips_data_all.fhv_external`
OPTIONS (
 format = 'PARQUET',
 uris = ['gs://dtc_data_lake_aqueous-abbey-375520/data/fhv/fhv_tripdata_2019-*.parquet']
);

-- Count External Table

SELECT COUNT(*) FROM `trips_data_all.fhv_external`; 

-- Ingestion Internal Table

CREATE OR REPLACE TABLE `aqueous-abbey-375520.trips_data_all.fhv_internal` AS
SELECT * FROM `aqueous-abbey-375520.trips_data_all.fhv_external`;

-- Count Internal Table

SELECT COUNT(*) FROM `trips_data_all.fhv_internal`; 
```

Result: 43,244,696


### Question 2

Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

#### Answer

```sql
-- EXTERNAL: distinct number of affiliated_base_number 

SELECT COUNT(DISTINCT affiliated_base_number) FROM `trips_data_all.fhv_external`; 

-- INTERNAL: distinct number of affiliated_base_number 

SELECT COUNT(DISTINCT affiliated_base_number) FROM `trips_data_all.fhv_internal`; 
```


- 25.2 MB for the External Table and 100.87MB for the BQ Table
- 225.82 MB for the External Table and 47.60MB for the BQ Table
- 0 MB for the External Table and 0MB for the BQ Table
- `0 MB for the External Table and 317.94MB for the BQ Table`

### Question 3: How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?

- `717,748`
- 1,215,687
- 5
- 20,332

```sql
SELECT COUNT(*) 
FROM `trips_data_all.fhv_internal`
WHERE PUlocationID IS NULL AND DOlocationID IS NULL;
```

### Question 4: What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

- Cluster on pickup_datetime Cluster on affiliated_base_number
- `Partition by pickup_datetime Cluster on affiliated_base_number`
- Partition by pickup_datetime Partition by affiliated_base_number
- Partition by affiliated_base_number Cluster on pickup_datetime

```sql
-- Partition by Date and Cluster by Affiliated_Base_Number
CREATE OR REPLACE TABLE `aqueous-abbey-375520.trips_data_all.fhv_internal_partitioned` AS
PARTITION BY DATE(pickup_datetime) 
CLUSTER BY Affiliated_Base_Number AS
SELECT * FROM `aqueous-abbey-375520.trips_data_all.fhv_external`;
```

### Question 5: Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).

- 12.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table
- 582.63 MB for non-partitioned table and 0 MB for the partitioned table
- `646.25 MB for non-partitioned table and 646.25 MB for the partitioned table`

```sql
-- Partition by Date and Cluster by Affiliated_base_number
CREATE OR REPLACE TABLE `aqueous-abbey-375520.trips_data_all.fhv_internal_partitioned`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT * FROM `aqueous-abbey-375520.trips_data_all.fhv_internal`;

-- Estimated bytes processed by partitioned table: 647.87
SELECT DISTINCT Affiliated_base_number
FROM `aqueous-abbey-375520.trips_data_all.fhv_internal_partitioned`
WHERE pickup_datetime BETWEEN TIMESTAMP('2019/03/01 00:00:00') AND TIMESTAMP('2019/03/31 23:59:59');

-- Estimated bytes processed by non-partitioned table: 647.87
SELECT DISTINCT Affiliated_base_number
FROM `aqueous-abbey-375520.trips_data_all.fhv_internal`
WHERE pickup_datetime BETWEEN TIMESTAMP('2019/03/01 00:00:00') AND TIMESTAMP('2019/03/31 23:59:59');

```

### Question 6: Where is the data stored in the External Table you created?

- Big Query
- `GCP Bucket`
- Container Registry
- Big Table

### This weeks help

These won't work. You need to make sure you use Int64: 

```python
# Incorrect:
df['DOlocationID'] = pd.to_numeric(df['DOlocationID'], downcast=integer) or
df['DOlocationID'] = df['DOlocationID'].astype(int)
# Correct:
df['DOlocationID'] = df['DOlocationID'].astype('Int64')
```

### Social Media Links

https://twitter.com/sbstn2809/status/1625203273451069440
https://www.facebook.com/seduerr/posts/pfbid0CPGvz7Rpd2BL6EYWxQgvnBp4D82corJHxS3AnEdeLtURxap3AtftcaCTobDovCxWl
