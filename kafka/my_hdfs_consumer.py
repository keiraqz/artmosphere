import time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
import os


class Consumer(object):
    """Kafka consumer class with functions to consume messages to HDFS.
    Messages are blocked into 20MB files and transferred to HDFS in two
    folders, /user/PuppyPlaydate/history/ and /user/PuppyPlaydate/cached.
    /history/ will contain all immutable files in the case of needing to
    rebuild the entire batch view. /cached/ will be deleted on a daily basis
    for the incremental batch job.
    Attributes:
        client: string representing IP:port of the kafka broker
        consumer: Consumer object specifying the client group, and topic
        temp_file_path: location of the 20MB file to be appended to before
            transfer to HDFS
        temp_file: File object opened from temp_file_path
        topic: String representing the topic on Kafka
        group: String representing the Kafka consumer group to be associated
            with
        block_cnt: integer representing the block count for print statements
    """
    def __init__(self, addr, group, topic):
        """Initialize Consumer with kafka broker IP, group, and topic."""
        self.client = KafkaClient(addr)
        self.consumer = SimpleConsumer(self.client, group, topic,
                                       max_buffer_size=1310720000)
        self.temp_file_path = None
        self.temp_file = None
        self.hadoop_path = "/insight/pinterest/history"
        # self.cached_path = "/insight/pinterest/cache"
        self.topic = topic
        self.group = group
        self.block_cnt = 0

    def consume_topic(self, output_dir):
        """Consumes a stream of messages from the "messages" topic.
        Code template from https://github.com/ajmssc/bitcoin-inspector.git
        Args:
            output_dir: string representing the directory to store the 20MB
                before transferring to HDFS
        Returns:
            None
        """
        timestamp = time.strftime('%Y%m%d%H%M%S')
        
        # open file for writing
        self.temp_file_path = "%s/kafka_%s_%s_%s.dat" % (output_dir,
                                                         self.topic,
                                                         self.group,
                                                         timestamp)
        self.temp_file = open(self.temp_file_path,"w")

        while True:
            try:
                # get 5 messages at a time, non blocking
                messages = self.consumer.get_messages(count=5, block=False)
                # OffsetAndMessage(offset=43, message=Message(magic=0,
                # attributes=0, key=None, value='some message'))
                for message in messages:
                    self.temp_file.write(message.message.value + "\n")

                # file size > 20MB

                # if self.temp_file.tell() > 20000000:
                    self.flush_to_hdfs(output_dir)

                self.consumer.commit()
            except:
                # move to tail of kafka topic if consumer is referencing
                # unknown offset
                self.consumer.seek(0, 2)


    def flush_to_hdfs(self, output_dir):
        """Flushes the 20MB file into HDFS.
        Code template from https://github.com/ajmssc/bitcoin-inspector.git
        Flushes the file into two folders under
        hdfs://user/PuppyPlaydate/history and
        hdfs://user/PuppyPlaydate/cached
        Args:
            output_dir: string representing the directory to store the 20MB
                before transferring to HDFS
        Returns:
            None
        """
        self.temp_file.close()

        timestamp = time.strftime('%Y%m%d%H%M%S')


        hadoop_fullpath = "%s/%s_%s_%s.dat" % (self.hadoop_path, self.group,
                                               self.topic, timestamp)
        # cached_fullpath = "%s/%s_%s_%s.dat" % (self.cached_path, self.group,
        #                                        self.topic, timestamp)
        print "Block {}: Flushing data file to HDFS => {}".format(str(self.block_cnt),
                                                                  hadoop_fullpath)
        self.block_cnt += 1

        # place blocked messages into history and cached folders on hdfs
        # os.system("sudo -u hdfs hdfs dfs -put %s %s" % (self.temp_file_path,
        #                                                 hadoop_fullpath))
        os.system("hdfs dfs -put %s %s" % (self.temp_file_path, hadoop_fullpath))        
        # os.system("sudo -u hdfs hdfs dfs -put %s %s" % (self.temp_file_path,
        #                                                 cached_fullpath))
        os.remove(self.temp_file_path)

        timestamp = time.strftime('%Y%m%d%H%M%S')

        self.temp_file_path = "%s/kafka_%s_%s_%s.dat" % (output_dir,
                                                         self.topic,
                                                         self.group,
                                                         timestamp)
        self.temp_file = open(self.temp_file_path, "w")


if __name__ == '__main__':

    print "\nConsuming messages..."
    cons = Consumer(addr="ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9092", group="hdfs-01", topic="pinterest")
    cons.consume_topic("/home/ubuntu/Artmo/kafka/kafka_messages")