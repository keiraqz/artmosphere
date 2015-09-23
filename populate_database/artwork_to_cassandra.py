'''
Created on Sep 21, 2015

@author: Shanghai
'''

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
        # self.bulk_data = []
        # self.INDEX_NAME = 'artsy'
        # self.TYPE_NAME = 'artworks'
        # self.ID_FIELD = 'id'
        self.hdfs_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/artworks"
        # self.hdfs_path_gene = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/artwork_info/gene"

    # def get_gene_id_list(self,link,artwork_id):
    #     local_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/artwork_info/gene/%s.json" % artwork_id
    #     id_list = []
    #     try:
    #         local_df = sqlContext.read.json(local_path)
    #         local_df.map(lambda x:x.id).collect()
    #         # id_list = ', '.join([str(x) for x in local_df])
    #         id_list.append(local_df)
    #     except:
    #         id_list = []
    #     return id_list

    # def get_artist_id_list(self,link,artwork_id):
    #     local_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/artwork_info/artist/%s.json" % artwork_id
    #     id_list = []
    #     try:
    #         local_df = sqlContext.read.json(local_path)
    #         local_df.map(lambda x:x.id).collect()
    #         # id_list = ', '.join([str(x) for x in local_df])
    #         id_list.append(local_df)
    #     except:
    #         id_list = []
    #     return id_list
    def get_map(self, x):
        if x._links.thumbnail.href != "":
            return lambda x: {"artwork_id": x.id,"title":x.title, "collecting_institution":x.collecting_institution, "created_at":x.created_at, "image_link":x._links.thumbnail.href,"sold":str(x.sold),"pined_count":random.gauss(100, 5)}
        else:
            return lambda x: {"artwork_id": x.id,"title":x.title, "collecting_institution":x.collecting_institution, "created_at":x.created_at, "image_link":"none","sold":str(x.sold),"pined_count":random.gauss(100, 5)}

if __name__ == '__main__':
    conf = SparkConf().setAppName("JSON Ingest")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    cf = LoadJson()
    df = sqlContext.read.json(cf.hdfs_path)
    # df_RDD = df.map(cf.get_map)
    df_RDD = df.map(lambda x: {"artwork_id": x.id,"title":x.title, "collecting_institution":x.collecting_institution, "created_at":x.created_at, "image_link":x._links.thumbnail.href,"sold":str(x.sold),"pined_count":random.gauss(100, 5)})
    # print df_RDD.first()

    # gene_df = sqlContext.read.json(cf.hdfs_path_gene)
    # gene_id_RDD = gene_df.map(lambda x: x.id).foreach(???)
    df_RDD.saveToCassandra("art_pin_log","artworks")

