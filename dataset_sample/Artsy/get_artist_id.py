'''
Created on Sep 19, 2015

@author: Keira Zhou
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

data=[]
artwork_list = sqlContext.read.json(path)
all_ids = artwork_list.map(lambda x: x.id)
ids = all_ids.collect()
target = open(idlist, 'w')

for id in ids:
  target.write("%s\n" % id)
