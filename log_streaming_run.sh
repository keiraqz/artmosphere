#!/bin/bash

'date'
spark-submit --class UserDataStreaming --master spark://ip-172-31-11-230:7077 --jars spark_streaming/target/scala-2.10/artsy_data-assembly-1.0.jar spark_streaming/target/scala-2.10/artsy_data_2.10-1.0.jar
'date'
