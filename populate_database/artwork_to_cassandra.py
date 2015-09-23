'''
Created on Sep 21, 2015

@author: Shanghai
'''
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import pyspark_cassandra
import pyspark_cassandra.streaming
from pyspark_cassandra import CassandraSparkContext
import pyspark
import pyspark.sql
from pyspark import *
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
import json
import csv
import urllib2
import sys
import random

class LoadJson(object):
    def __init__(self):
        self.hdfs_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/artworks"

if __name__ == '__main__':
    conf = SparkConf().setAppName("JSON Ingest")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    schema = avro.schema.parse(open("/home/ubuntu/Artmo/populate_database/artwork_schema.avro").read())
    cf = LoadJson()
    df = sqlContext.read.json(cf.hdfs_path)
    df_RDD = df.map(lambda x: {"artwork_id": x.id,"title":x.title, "collecting_institution":x.collecting_institution, "created_at":x.created_at, "image_link":x._links.thumbnail.href,"sold":str(x.sold),"pined_count":random.gauss(100, 5)})
    df_RDD.saveToCassandra("art_pin_log","artworks")

