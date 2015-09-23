# from pyspark import SparkContext, SparkConf
# from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
from elasticsearch import Elasticsearch
import json
import csv
import urllib2
import sys


source_file = '/mnt/my-data/datasets/pinterest/pinterest_small.csv'

ES_HOST = {"host" : "localhost", "port" : 9200}

INDEX_NAME = 'pinterest'
TYPE_NAME = 'pin'
ID_FIELD = 'pin_id'

with open(source_file, 'rU') as csvfile:

# response = urllib2.urlopen(FILE_URL)
	csv_file_object = csv.reader(csvfile)
	header = csv_file_object.next()
	header = [item.lower() for item in header]

	bulk_data = [] 

	for row in csv_file_object:
		data_dict = {}
		for i in range(len(row)):
			# print header[i]
			if i == 0:
				data_dict[header[i]] = float(row[i])
			else:
				data_dict[header[i]] = row[i]
		op_dict = {
			"index": {
				"_index": INDEX_NAME,
				"_type": TYPE_NAME,
				"_id": data_dict[ID_FIELD]
			}
		}
		bulk_data.append(op_dict)
		bulk_data.append(data_dict)

csvfile.close()

#create ES client, create index
es = Elasticsearch(hosts = [ES_HOST])

if es.indices.exists(INDEX_NAME):
	print("deleting '%s' index..." % (INDEX_NAME))
	res = es.indices.delete(index = INDEX_NAME)
	print(" response: '%s'" % (res))

# since we are running locally, use one shard and no replicas
request_body = {
	"settings" : {
		"number_of_shards": 1,
		"number_of_replicas": 0
	}
}

print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))

# bulk index the data
print("bulk indexing...")
res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)

# sanity check
res = es.search(index = INDEX_NAME, q='description:"to"', body={"query": {"match_all": {}}})
print(" response: '%s'" % (res))

print("results:")
for hit in res['hits']['hits']:
	print(hit["_source"])