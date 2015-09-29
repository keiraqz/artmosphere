'''
Created on Sep 21, 2015
@author: Keira Zhou
'''

import pyspark_cassandra
import pyspark_cassandra.streaming
from pyspark_cassandra import CassandraSparkContext
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
import json
import csv
import urllib2
import sys


class LoadJson(object):
    def __init__(self):
        '''Save artist information to cassandra'''
        self.hdfs_path = "hdfs://ec2-54-215-136-187.us-west-1.compute.amazonaws.com:9000/insight/artsy/artists"


if __name__ == '__main__':
    conf = SparkConf()
    # .setAppName("JSON Ingest")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    cf = LoadJson()
    df = sqlContext.read.json(cf.hdfs_path)
    df_RDD = df.map(lambda x: {"artist_id": x.id,"name":x.name,"location":x.location})
    df_RDD.saveToCassandra("art_pin_log","artists")
