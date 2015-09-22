import csv 
import pycassa
from cassandra.cluster import Cluster

cluster = Cluster(['172.31.11.233', '172.31.11.231','172.31.11.232'])
session = cluster.connect('art_pin_log')

with open('/mnt/my-data/datasets/artsy/all_genes.csv', 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		session.execute("INSERT INTO genes (artsy_id,artsy_slug,artsy_url,definition,type) VALUES (%s,%s,%s,%s,%s)", (row["artsy_id"],row["artsy_slug"],row["artsy_url"],row["definition"],row["type"]))



    