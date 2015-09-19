from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
from elasticsearch import Elasticsearch
import json
import csv
import urllib2
import sys

sc = SparkContext()


# FILE_URL = "hdfs://localhost:9000/insight/pinterest/pinterest_small.csv"
souce_file = sc.textFile("hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/pinterest/pinterest_small.csv")

header = souce_file.take(1)[0]
rows = souce_file.filter(lambda line: line != header)

print rows.count()


# ES_HOST = {"host" : "localhost", "port" : 9200}

# INDEX_NAME = 'pinterest'
# TYPE_NAME = 'pins'
# ID_FIELD = 'pin_id'


# response = urllib2.urlopen(souce_file)


# csv_file_object = csv.reader(response)
 
# header = csv_file_object.next()
# header = [item.lower() for item in header]

# bulk_data = [] 

# for row in csv_file_object:
# 	data_dict = {}
# 	for i in range(len(row)):
# 		data_dict[header[i]] = row[i]
# 	op_dict = {
# 		"index": {
# 			"_index": INDEX_NAME,
# 			"_type": TYPE_NAME,
# 			"_id": data_dict[ID_FIELD]
# 		}
# 	}
# 	bulk_data.append(op_dict)
# 	bulk_data.append(data_dict)

# #create ES client, create index
# es = Elasticsearch(hosts = [ES_HOST])

# if es.indices.exists(INDEX_NAME):
# 	print("deleting '%s' index..." % (INDEX_NAME))
# 	res = es.indices.delete(index = INDEX_NAME)
# 	print(" response: '%s'" % (res))

# # since we are running locally, use one shard and no replicas
# request_body = {
# 	"settings" : {
# 		"number_of_shards": 1,
# 		"number_of_replicas": 0
# 	}
# }

# print("creating '%s' index..." % (INDEX_NAME))
# res = es.indices.create(index = INDEX_NAME, body = request_body)
# print(" response: '%s'" % (res))

# # bulk index the data
# print("bulk indexing...")
# res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)

# # sanity check
# res = es.search(index = INDEX_NAME, size=2, body={"query": {"match_all": {}}})
# print(" response: '%s'" % (res))

# print("results:")
# for hit in res['hits']['hits']:
# 	print(hit["_source"])