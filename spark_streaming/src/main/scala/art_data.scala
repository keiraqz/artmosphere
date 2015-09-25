import kafka.serializer.StringDecoder
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.sql._
import com.datastax.spark.connector._
import com.datastax.spark.connector.streaming._
import com.datastax.spark.connector.cql.{ColumnDef, RegularColumn, TableDef}
import com.datastax.spark.connector.types.IntType
import com.datastax.spark.connector.writer._
import org.apache.cassandra.serializers.TimestampSerializer
import java.util.Date
import org.joda.time.DateTime
import org.joda.time.format.DateTimeFormat
// import datetime

object UserDataStreaming {
  def main(args: Array[String]) {

    val brokers = "ec2-52-8-247-28.us-west-1.compute.amazonaws.com:9092,ec2-54-183-69-4.us-west-1.compute.amazonaws.com:9092,ec2-52-8-244-245.us-west-1.compute.amazonaws.com:9092,ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9092"
    val topics = "pin_activity"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("art_data").set("spark.cassandra.connection.host", "172.31.11.232")
    // val sc = new SparkContext(sparkConf)
    val ssc = new StreamingContext(sparkConf, Seconds(30))

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)
    // val format = new java.text.SimpleDateFormat("yyyy-mm-dd HH:mm")
   
    // Get the lines and show results
    messages.foreachRDD { rdd =>

        val sqlContext = SQLContextSingleton.getInstance(rdd.sparkContext)
        import sqlContext.implicits._
        // val current_time = format.format(new java.util.Date())
        val current_time = TimestampFormatter.format(new Date())

        val lines = rdd.map(_._2)
        val ticksDF = lines.map( x => {
                                  val tokens = x.split(";")
                                  Tick(tokens(0), tokens(2), tokens(3), tokens(4))}).toDF()
        // val ticks_per_source_DF = ticksDF.map(x => (x,1)).reduceByKey(_ + _).collect()
        val ticks_per_source_DF = ticksDF.groupBy("art_id").count().collect()
        var ticks_with_time = ticks_per_source_DF.map(x => (x(0),current_time,x(1)))

        rdd.sparkContext.parallelize(ticks_with_time).saveToCassandra("art_pin_log", "artwork_count", SomeColumns("art_id","event_time", "pin_count"))
    }

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}

case class Tick(source: String, usr_id: String, action: String, art_id: String)
// case class Astamp(artwork: String, timestamp: String, count: Integer)

/** Lazily instantiated singleton instance of SQLContext */
object SQLContextSingleton {

  @transient  private var instance: SQLContext = _

  def getInstance(sparkContext: SparkContext): SQLContext = {
    if (instance == null) {
      instance = new SQLContext(sparkContext)
    }
    instance
  }
}

object TimestampFormatter {

  private val TimestampPattern = "yyyy-MM-dd'T'HH:mm:ssZ"

  def format(date: Date): String =
    DateTimeFormat.forPattern(TimestampPattern).print(new DateTime(date.getTime))
}