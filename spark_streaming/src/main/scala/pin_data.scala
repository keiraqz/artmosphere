import kafka.serializer.StringDecoder

import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._

object PinterestDataStreaming {
  def main(args: Array[String]) {

    val brokers = "ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9092"
    val topics = "pinterest"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("pinterest_data")
    val ssc = new StreamingContext(sparkConf, Seconds(2))

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)

    // Get the lines and show results
    messages.foreachRDD { rdd =>

        val sqlContext = SQLContextSingleton.getInstance(rdd.sparkContext)
        import sqlContext.implicits._
        println(rdd.first())
        val lines = rdd.map(_._2)
        val ticksDF = lines.map( x => {
                                  val tokens = x.split(",")
                                  Tick(tokens(0).toInt, tokens(2), tokens(19))}).toDF()
        // val ticks_per_source_DF = ticksDF.groupBy("pin_id")
        //                         .agg("price" -> "avg", "volume" -> "sum")
        //                         .orderBy("pin_id")

        // ticks_per_source_DF.show()
        ticksDF.show()
    }

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}

case class Tick(pin_id: Int, descpt: String, link: String)

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