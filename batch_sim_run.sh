#!/bin/bash

'date'
$SPARK_HOME/bin/pyspark --master spark://ip-172-31-11-230:7077 --packages TargetHolding:pyspark-cassandra:0.1.5     --conf spark.cassandra.connection.host="172.31.11.233,172.31.11.231,172.31.11.232" ~/Artmo/batch_similarity/compute_similarity.py
'date'
