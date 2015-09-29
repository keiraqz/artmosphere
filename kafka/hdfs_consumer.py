import time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
import os


class Consumer(object):
    def __init__(self, addr, group, topic):
        """Initialize Consumer with kafka broker IP, group, and topic."""
        self.client = KafkaClient(addr)
        self.consumer = SimpleConsumer(self.client, group, topic,
                                       max_buffer_size=1310720000)
        self.temp_file_path = None
        self.temp_file = None
        self.hadoop_path = "/insight/artsy/geo"
        self.topic = topic
        self.group = group
        self.block_cnt = 0

    def consume_topic(self, output_dir):
        """Consumes a stream of messages from the "post_geo_activity" topic.
        Code template from https://github.com/ajmssc/bitcoin-inspector.git
        """
        timestamp = time.strftime('%Y%m%d%H%M%S')
        
        # open file for writing
        self.temp_file_path = "%s/kafka_%s_%s_%s.dat" % (output_dir,self.topic,self.group,timestamp)
        self.temp_file = open(self.temp_file_path,"w")

        while True:
            try:
                # get 1000 messages at a time, non blocking
                messages = self.consumer.get_messages(count=1000, block=False)
                for message in messages:
                    self.temp_file.write(message.message.value + "\n")

                # file size > 20MB
                if self.temp_file.tell() > 20000000:
                    self.flush_to_hdfs(output_dir)

                self.consumer.commit()
            except:
                # move to tail of kafka topic if consumer is referencing
                # unknown offset
                self.consumer.seek(0, 2)


    def flush_to_hdfs(self, output_dir):
        """Flushes the 20MB file into HDFS."""
        self.temp_file.close()
        timestamp = time.strftime('%Y%m%d%H%M%S')
        hadoop_fullpath = "%s/%s_%s_%s.dat" % (self.hadoop_path, self.group,self.topic, timestamp)

        print "Block {}: Flushing data file to HDFS => {}".format(str(self.block_cnt),hadoop_fullpath)
        self.block_cnt += 1
        os.system("hdfs dfs -put %s %s" % (self.temp_file_path, hadoop_fullpath)) # save from local to hdfs
        os.remove(self.temp_file_path) # remove temp local file
        timestamp = time.strftime('%Y%m%d%H%M%S')
        self.temp_file_path = "%s/kafka_%s_%s_%s.dat" % (output_dir,self.topic,self.group,timestamp)
        self.temp_file = open(self.temp_file_path, "w")


if __name__ == '__main__':
    print "\nConsuming messages..."
    cons = Consumer(addr="ec2-52-8-247-28.us-west-1.compute.amazonaws.com:9092,ec2-54-183-69-4.us-west-1.compute.amazonaws.com:9092,ec2-52-8-244-245.us-west-1.compute.amazonaws.com:9092,ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9092", group="hdfs", topic="post_geo_activity")
    cons.consume_topic("/mnt/my-data/kafka/kafka_messages_geo")



