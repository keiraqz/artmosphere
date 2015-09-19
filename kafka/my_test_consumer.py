import time
from kafka.client import KafkaClient
from kafka.consumer import *
import os

kafka = KafkaClient("localhost:9092")

print("After connecting to kafka")

consumer = SimpleConsumer(kafka, "hdfs-00", "pinterest")

for message in consumer:
    print(message)







# kafka = KafkaClient("localhost:9092")
# # output_dir = "/home/ubuntu/Artmo/kafka/kafka_messages"
# # topic = "pinterest"
# # group = "hdfs"

# print("After connecting to kafka")

# consumer = SimpleConsumer(kafka, "hdfs", "pinterest")
# # timestamp = time.strftime('%Y%m%d%H%M%S')
# # temp_file_path = "%s/kafka_%s_%s_%s.dat" % (output_dir,
# #                                             topic,
# #                                             group,
# #                                             timestamp)
# # temp_file = open(temp_file_path,"w")

# for message in consumer:
#     print(message)
#     # temp_file.write(message.message.value + "\n")