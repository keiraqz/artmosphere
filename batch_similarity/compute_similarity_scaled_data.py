'''
Created on Sep 22, 2015

@author: Shanghai
'''

import pyspark_cassandra
import pyspark_cassandra.streaming
from pyspark_cassandra import CassandraSparkContext
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from uuid import uuid1
import json
import csv
import urllib2
import sys
import os
import time
import hdfs


class ComputeSimilarity(object):
    def __init__(self):
        self.hdfs_path = ""
        self.temp_file_path = ""

    def compute_similarity(self,df):
        ''' 
        parse [{a1,[g1,g2,g3]}, {a2,[g1,g3,g4]}, {a4,[g1,g2,g4]}...]
        into [(g1,a1),(g1,a2),(g1,a3),(g2,a1),(g2,a2),(g2,a4)....]
        ''' 
        df_RDD_1 = df.flatMap(lambda x: [(str(y.strip("u'[ ]")),str(x.artworks)) for y in (x.gene).split(",")])  

        ''' 
        RDD join itself on Gene_id to get artwork pair
        RDD_1_join output: {gene_id , (artwork1, artwork2)} => {(artwork1, artwork2),1}
        RDD_1_count output: {(artwork1, artwork2), <count>}
        RDD_1_map output: (artwork1, artwork2, <count>)
        '''
        RDD_1_join = df_RDD_1.join(df_RDD_1).map(lambda x: (x[1],1))
        RDD_1_count = RDD_1_join.reduceByKey(lambda a, b: a + b)
        RDD_1_map = RDD_1_count.map(lambda x: (x[0][0],x[0][1],x[1])).filter(lambda x: x[0]!=x[1])
        RDD_1_save = RDD_1_map.map(lambda x: {"id_1":x[0],"id_2":x[1],"sim_count":str(x[2])})

        ''' save result '''
        self.save_to_cassandra(RDD_1_save)
        print("Spark saved to Cassandra: %s\n" % time.strftime('%Y%m%d%H%M%S'))
        self.save_to_hdfs(RDD_1_save)
        print("Spark saved to HDFS: %s\n" % time.strftime('%Y%m%d%H%M%S'))

    def save_to_cassandra(self,RDD_1_save):
        ''' save to Cassandra '''
        RDD_1_save.saveToCassandra("art_pin_log","art_sim_fake")

    def save_to_hdfs(self,RDD_1_save):
        ''' save to HDFS '''
        timestamp = time.strftime('%Y%m%d%H%M%S')
        path = "%s/art_art_sim_%s.json" % (self.temp_file_path,timestamp)
        RDD_1_save.saveAsTextFile(path)


if __name__ == '__main__':
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    cf = ComputeSimilarity()
    cf.hdfs_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/engr_gene/a5000_g20.json"
    cf.temp_file_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/temp"
    print("Spark loading data: %s\n" % time.strftime('%Y%m%d%H%M%S'))
    df = sqlContext.read.json(cf.hdfs_path)
    print("Spark starting computation: %s\n" % time.strftime('%Y%m%d%H%M%S'))
    cf.compute_similarity(df)

    

    

