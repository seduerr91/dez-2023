# Week 6 Streaming With Kafka

## Homework

### Question  1:  Please select the statements that are correct
- `Kafka Node is responsible to store topics`
- `Zookeeper is removed form Kafka cluster starting from version 4.0`
- `Retention configuration ensures the messages not get lost over specific period of time.`
- `Group-Id ensures the messages are distributed to associated consumers`

### Question 2: Please select the Kafka concepts that support reliability and availability

- `Topic Replication`
- Topic Paritioning
- Consumer Group Id
- `Ack All`

### Question 3: Please select the Kafka concepts that support scaling

- Topic Replication
- `Topic Partitioning`
- `Consumer Group Id`
- Ack All

### Question 4: Please select the attributes that are good candidates for partitioning key. Consider cardinality of the field you have selected and scaling aspects of your application

- `payment_type`
- `vendor_id`
- `passenger_count`
- total_amount
- tpep_pickup_datetime
- tpep_dropoff_datetime

### Question 5:  Which configurations below should be provided for Kafka Consumer but not needed for Kafka Producer

- `Deserializer Configuration`
- `Topics Subscription`
- Bootstrap Server
- `Group-Id`
- `Offset`
- Cluster Key and Cluster-Secret

### Question 6: Optional

- Did not do this one.

## Most answers came from

- The Youtube Videos
- Dataengs great [summary](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/6_streaming.md#)
- The Stream [book](https://www.gentlydownthe.stream/)

## Seb Help

Literally, the best resource to study Kafka: <https://www.gentlydownthe.stream/>
Screenshot: ![help seb 6](img/week_6_seb_help.png)

## Public Sharing

- [Twitter Week 6](https://twitter.com/sbstn2809/status/1633304870680920064)
