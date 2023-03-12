# Docker Network

## Setup Postgres + PGAdmin

In Docker set up a network to host both a "postgres database" and a "pgAdmin instance" in a network by using docker compose to interact with it in a visual PGADMIN front-end with:

docker-compose up -d

(-d = detached, so that you can continue using that terminal).

## Ingest the database with base data

Get the name of the network with: docker network ls to adapt it in the following script. Ingest the database with the first data to table yellow taxi with the Dockerfile in 2 steps.

First, create an image from the Dockerfile: docker build -t taxi_ingest:v001 .
Second, run the Docker image: 
```bash
docker run -it \
    --network=3_seb_default  \
    taxi_ingest:v001   \
    --user=root \
    --password=root \
    --host=3_seb_pgdatabase_1  \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz

```

## 2. Ingest the database with green trip data

Now, the code needs to be adapted as the columns tpep don't exist. Hence, go into ingest.py remove / comment out the respective instructions and build a fresh Docker image. 

Step1, docker build -t taxi_ingest:v002 .
Second, run the Docker image:
docker run -it \
    --network=3_seb_default  \
    taxi_ingest:v002   \
    --user=root \
    --password=root \
    --host=3_seb_pgdatabase_1  \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz

docker run -it \
    --network=3_seb_default  \
    taxi_ingest:v002   \
    --user=root \
    --password=root \
    --host=3_seb_pgdatabase_1  \
    --port=5432 \
    --db=ny_taxi \
    --table_name=lookupzones \
    --url=https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

## Clean up

docker rm `docker ps -q -f status=exited`
docker rm `docker ps -q -f status=created`

## Query to get all trips from the green_taxi_trips table

### Question 3.

SELECT COUNT(*)
FROM green_taxi_trips
WHERE
 TO_DATE(lpep_pickup_datetime,'YYYY-MM-DD') = '2019-01-15'
 AND TO_DATE(lpep_dropoff_datetime,'YYYY-MM-DD') = '2019-01-15';

that returns: '20530'

### Question 4. Largest trip for each day - Which was the day with the largest trip distance Use the pick up time for your calculations?

2019-01-18: 76829.3600000002
2019-01-28: 74053.50000000006
2019-01-15: 74856.25999999995
2019-01-10: 79530.83000000006

Code for solution

SELECT count(x) from green_taxi_trips
WHERE TO_DATE(lpep_pickup_datetime,'YYYY-MM-DD') = '2019-01-01'
AND passenger_count = 2;

SELECT count(x) from green_taxi_trips
WHERE TO_DATE(lpep_pickup_datetime,'YYYY-MM-DD') = '2019-01-01'
AND passenger_count = 3;

### Question 5. The number of passengers

2 passengers: 1282; 3 passengers: 254

SELECT passenger_count from green_taxi_trips
WHERE TO_DATE(lpep_pickup_datetime,'YYYY-MM-DD') = '2019-01-01';

### Question 6. Largest tip

Start: 7 - Astoria Zone

Ended in: 
43 - Central Park - 112.63 USD
130 - Jamaica - 89.43
216 - South Ozone Park - 26.08
146 - Long Island City/Queens Plaza - 800.31

SELECT * from green_taxi_trips
WHERE pulocationid = 7 AND dolocationid = 43;

SELECT * from green_taxi_trips
WHERE pulocationid = 7 AND dolocationid = 130;

SELECT * from green_taxi_trips
WHERE pulocationid = 7 AND dolocationid = 216;

SELECT * from green_taxi_trips
WHERE pulocationid = 7 AND dolocationid = 146;

DONE ON A MACBOOK PRO
