#!/bin/bash

'date'
spark-submit --class GeoData --master spark://ip-172-31-11-230:7077 --jars /home/ubuntu/Artmo/batch_geo/target/scala-2.10/geo_data-assembly-1.0.jar /home/ubuntu/Artmo/batch_geo/target/scala-2.10/geo_data_2.10-1.0.jar
'date'
