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
import random
# from pprint import pprint

class LoadJson(object):

    def __init__(self):
        self.bulk_data = []
        self.INDEX_NAME = 'artsy'
        self.TYPE_NAME = 'artworks'
        self.ID_FIELD = 'id'
        self.hdfs_path = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/artworks/artwork_1.txt"


    # def to_bulk(self,x):
    #     tem = []
    #     op_dict = {
    #         "index": {
    #             "_index": self.INDEX_NAME,
    #             "_type": self.TYPE_NAME,
    #             # "_id": data_dict[ID_FIELD]
    #         }
    #     }
    #     tem.append(op_dict)
    #     tem.append(x)
    #     return tem

if __name__ == '__main__':
    conf = SparkConf().setAppName("ES Ingest")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)

    cf = LoadJson()
    df = sqlContext.read.json(cf.hdfs_path)

    # print df.toJSON().first()
    temp = df.map(lambda x: {"artwork_id": x.id,"title":x.title, "image_link":x._links.thumbnail.href,"collecting_institution":x.collecting_institution, "created_at":x.created_at, "sold":str(x.sold),"pined_count":random.gauss(100, 5)}).collect()
    op_dict = {
        "index": {
            "_index": cf.INDEX_NAME,
            "_type": cf.TYPE_NAME,
            # "_id": data_dict[ID_FIELD]
        }
    }
    for idd in temp:
        cf.bulk_data.append(op_dict)
        cf.bulk_data.append(idd)

    # cf.bulk_data.first()
    ES_HOST = {"host" : "localhost", "port" : 9200}
    es = Elasticsearch(hosts = [ES_HOST])
    if es.indices.exists(cf.INDEX_NAME):
        print("deleting '%s' index..." % (cf.INDEX_NAME))
        res = es.indices.delete(index = cf.INDEX_NAME)
        print(" response: '%s'" % (res))

    request_body = {
        "settings" : {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }

    print("creating '%s' index..." % (cf.INDEX_NAME))
    res = es.indices.create(index = cf.INDEX_NAME, body = request_body)
    print(" response: '%s'" % (res))

    # bulk index the data
    print("bulk indexing...")

    res = es.bulk(index = cf.INDEX_NAME, body = cf.bulk_data, refresh = True)

    # sanity check
    res = es.search(index = cf.INDEX_NAME, size=2, body={"query": {"match_all": {}}})
    print(" response: '%s'" % (res))

    print("results:")
    for hit in res['hits']['hits']:
        print(hit["_source"])
