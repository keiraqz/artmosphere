import random
import sys
import six
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer
import json
from pprint import pprint

class Producer(object):

    def __init__(self, addr):
        self.client = KafkaClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, source_symbol):
        msg_cnt = 0
        while True:
            artwork_path = "loc.txt"
            with open(artwork_path) as f1:
                for line in f1:
                    if line.strip():
                        print line.strip()
                        self.producer.send_messages('post_geo_activity', source_symbol,line.strip())
                        msg_cnt += 1


if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key)