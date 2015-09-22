'''
Created on Sep 21, 2015

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


class ComputeSimilarity(object):
    def __init__(self):
        self.hdfs_path = ""


if __name__ == '__main__':
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    cf = ComputeSimilarity()
    cf.hdfs_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/gene_info.json"
    df = sqlContext.read.json(cf.hdfs_path)


    ''' 
    parse [{g1,[a1,a2,a3]}, {g2,[a1,a3,a4]}, {g4,[a1,a2,a4]}...]
    into [(g1,a1),(g1,a2),(g1,a3),(g2,a1),(g2,a2),(g2,a4)....]
    ''' 
    df_RDD_1 = df.flatMap(lambda x: [(str(x.gene),str(y.strip("u'[ ]"))) for y in (x.artworks).split(",")])  


    ''' 
    RDD join itself on Gene_id to get artwork pair
    RDD_1_join output: {gene_id , (artwork1, artwork2)} => {(artwork1, artwork2),1}
    RDD_1_count output: {(artwork1, artwork2), <count>}
    RDD_1_map output: (artwork1, artwork2, <count>)
    '''
    RDD_1_join = df_RDD_1.join(df_RDD_1).map(lambda x: (x[1],1))
    RDD_1_count = RDD_1_join.reduceByKey(lambda a, b: a + b)
    RDD_1_map = RDD_1_count.map(lambda x: (x[0][0],x[0][1],x[1])).filter(lambda x: x[0]!=x[1])
    

    ''' save to Cassandra '''
    RDD_1_save = RDD_1_map.map(lambda x: {"id_1":x[0],"id_2":x[1],"sim_count":str(x[2])})
    RDD_1_save.saveToCassandra("art_pin_log","artwork_sim")


 

