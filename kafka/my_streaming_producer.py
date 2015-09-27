import random
import sys
import six
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer

class Producer(object):

	def __init__(self, addr):
		self.client = KafkaClient(addr)
		self.producer = KeyedProducer(self.client)
		self.artist_id = []
		self.artwork_id = []

	def load_ids(self):
		artwork_path = "/home/ubuntu/Insight/dataset/Artsy/artwork_id.txt"
		artist_path = "/home/ubuntu/Insight/dataset/Artsy/artist_id.txt"
		with open(artwork_path) as f1:
			for line in f1:
				if line != "":
					self.artwork_id.append(line.strip())
			f1.close()
		with open(artist_path) as f2:
			for line in f2:
				if line != "":
					self.artist_id.append(line.strip())
			f2.close()


	def produce_msgs(self, source_symbol):
		msg_cnt = 0
		while True:
			time_field = datetime.now().strftime("%Y%m%d %H%M%S")
			user_field = random.choice(self.artist_id)
			art_field = random.choice(self.artwork_id)
			str_fmt = "{};{};{};{};{}"
			message_info = str_fmt.format(source_symbol,time_field,user_field,"pin",art_field)
			# print message_info
			self.producer.send_messages('pin_activity', source_symbol, message_info)
			msg_cnt += 1


if __name__ == "__main__":
	args = sys.argv
	ip_addr = str(args[1])
	partition_key = str(args[2])
	prod = Producer(ip_addr)
	prod.load_ids()
	prod.produce_msgs(partition_key)