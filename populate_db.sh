#!/bin/bash

'date'
# Save artists to Cassandra
$SPARK_HOME/bin/pyspark --master spark://ip-172-31-11-230:7077 --packages TargetHolding:pyspark-cassandra:0.1.5     --conf spark.cassandra.connection.host="172.31.11.233,172.31.11.231,172.31.11.232" ~/Artmo/populate_database/artists_to_cassandra.py

# Save artworks to Cassandra
$SPARK_HOME/bin/pyspark --master spark://ip-172-31-11-230:7077 --packages TargetHolding:pyspark-cassandra:0.1.5     --conf spark.cassandra.connection.host="172.31.11.233,172.31.11.231,172.31.11.232" ~/Artmo/populate_database/artwork_to_cassandra.py

# Save gene information to Cassandra
$SPARK_HOME/bin/pyspark --master spark://ip-172-31-11-230:7077 --packages TargetHolding:pyspark-cassandra:0.1.5     --conf spark.cassandra.connection.host="172.31.11.233,172.31.11.231,172.31.11.232" ~/Artmo/populate_database/gene_cassandra.py

# Save artowks to Elasticsearch
$SPARK_HOME/bin/pyspark --master spark://ip-172-31-11-230:7077  --jars ~/Downloads/elasticsearch-hadoop-2.1.0.Beta2.jar elasticsearch-json.py

'date'
