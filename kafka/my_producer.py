import os
import sys
from kafka import SimpleProducer, KafkaClient, KeyedProducer, SimpleConsumer
from datetime import datetime
import time

kafka = KafkaClient("54.183.55.185:9092")
source_file = '/home/ubuntu/Artmo/Dataset/Pinterest/pinterest_small.csv'

def genData(topic):
	# producer = KeyedProducer(kafka)
    producer = SimpleProducer(kafka)
    while True:
        with open(source_file) as f:
            for line in f:
                # key = line.split(" ")[0]
                # producer.send(topic, key, line.rstrip()) 
                producer.send_messages(topic, line)
                time.sleep(1)
        source_file.close()


genData("pinterest")
