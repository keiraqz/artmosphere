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
        self.location = []
        self.location_map = {}

    def load_ids(self):
        artwork_path = "/home/ubuntu/Insight/dataset/Country.json"
        with open(artwork_path) as f1:
            data = json.load(f1)
        f1.close()
        for val in data:
            self.location.append(val["code"])
            self.location_map[val["code"]]=val["name"]
        for i in range(1,20):
            self.location.append("GB")
        for i in range(1,25):
            self.location.append("ES")
        for i in range(1,15):
            self.location.append("DK")
        for i in range(1,10):
            self.location.append("US")
        for i in range(1,30):
            self.location.append("FR")
        for i in range(1,5):
            self.location.append("AU")
        for i in range(1,10):
            self.location.append("CN")

    def produce_msgs(self, source_symbol):
        msg_cnt = 0
        while True:
            time_field = datetime.now().strftime("%Y%m%d %H%M%S")
            location_field = random.choice(self.location)
            # str_fmt = "{};{};{};{};{}"
            # message_info = str_fmt.format(source_symbol,time_field,location_field,self.location_map[location_field],"post")
            message_info = '{"source":"%s","timestamp":"%s","code":"%s","location":"%s","action":"post"}' % (source_symbol,time_field,location_field,self.location_map[location_field])
            print message_info
            self.producer.send_messages('post_activity', source_symbol, str(message_info))
            msg_cnt += 1


if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.load_ids()
    prod.produce_msgs(partition_key)