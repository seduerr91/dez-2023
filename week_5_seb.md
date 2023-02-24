# Seb Notes Week 5 DEZ

## Remote connection via SSH

Maybe: `cd ~/.ssh; nano gcp` and then change the IP.

`ssh seb`

Then:

```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export JAVA_HOME="${HOME}/spark/jdk-11.0.1"
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${JAVA_HOME}/bin:${PATH}"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

Then: `jupyter notebook`

StructType(
    [
        types.StructField('HV0003', types.StringType(), True), 
        types.StructField('B027641', types.StringType(), True), 
        types.StructField('B027642', types.StringType(), True), 
        types.StructField('2021-05-31T23:53:49.000Z', types.TimestampType(), True), 
        types.StructField('2021-06-01T00:02:23.000Z', types.TimestampType(), True), 
        types.StructField('2021-06-01T00:02:41.000Z', types.TimestampType(), True), 
        types.StructField('2021-06-01T00:07:46.000Z', types.TimestampType(), True), 
        types.StructField('174', types.IntegerType(), True), 
        types.StructField('18', types.IntegerType(), True), 
        types.StructField('1.0', types.DoubleType(), True),
        types.StructField('305', types.IntegerType(), True), 
        types.StructField('8.13', types.DoubleType(), True), 
        types.StructField('0.012', types.DoubleType(), True), 
        types.StructField('0.24', types.DoubleType(), True), 
        types.StructField('0.72', types.DoubleType(), True), 
        types.StructField('0.015', types.DoubleType(), True), 
        types.StructField('0.016', types.DoubleType(), True), 
        types.StructField('0.017', types.DoubleType(), True), 
        types.StructField('7.03', types.DoubleType(), True), 
        types.StructField('N19', types.StringType(), True), 
        types.StructField('N20', types.StringType(), True), 
        types.StructField('_c21', types.StringType(), True), 
        types.StructField('N22', types.StringType(), True), 
        types.StructField('N23', types.StringType(), True)
    ]
)
