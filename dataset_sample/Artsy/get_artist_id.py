'''
Created on Sep 19, 2015

@author: Shanghai
'''

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
from elasticsearch import Elasticsearch
import json
import csv
import urllib2
import sys
import os

sc = SparkContext()
sqlContext = SQLContext(sc)


path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/artists"
idlist = "/home/ubuntu/Insight-dataset/Artsy/artist_id.txt"

# text_file = spark.textFile(idlist)
data=[]
# for dir_entry in os.listdir(path):
#     dir_entry_path = os.path.join(path, dir_entry)
#     if os.path.isfile(dir_entry_path):
artwork_list = sqlContext.read.json(path)
all_ids = artwork_list.map(lambda x: x.id)
#         for id in all_ids.collect():
ids = all_ids.collect()

target = open(idlist, 'w')

for id in ids:
  target.write("%s\n" % id)
