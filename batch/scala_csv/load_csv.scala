import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.elasticsearch.spark._

object load_csv {
 def main(args: Array[String]) {

   // setup the Spark Context named sc
   val conf = new SparkConf().setAppName("LoadCsv")
   val sc = new SparkContext(conf)

   // folder on HDFS to pull the data from
   // val folder_name = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/pinterest/pinterest_small.csv"
   val file_name = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/pinterest/pinterest_small.csv"


   // function to convert a timestamp to a 30 minute time slot
   def convert_to_30min(timestamp: String): String = {
       val min30 = timestamp.slice(11,13).toInt/30*30
       timestamp.take(11) + f"${min30}%02d" + "00"
   }

   // read in the data from HDFS
   // val file = sc.textFile(folder_name)
   val file = sc.textFile(file_name)

   // map each record into a tuple consisting of (time, price, volume)
   val pins = file.map(line => {
                        val record = line.split(",")
                       (record(0).toInt, record(1), record(2), record(3), record(4),
                        record(5), record(6).toInt, record(7).toInt, record(18), record(19))
                                })

   val pins = Map("pin_id" -> record._1, "pinner_id" -> record._2, "description" -> record._3,
      "board_id" -> record._4, "board_name" -> record._5, "source" -> record._6, 
      "likes_count" -> record._7, "repins_count" -> record._8, "pin_time" -> record._9, "image_link" -> record._10)


  sc.makeRDD(Seq(pins)).saveToEs("pinterest/pins")


  var output = sc.esRDD("radio/artists", "?description=c")



  // JobConf conf_0 = new JobConf();
  // conf_0.setInputFormat(EsInputFormat.class);
  // conf_0.set("es.resource", "pinterest/pins");

   // // apply the time conversion to the time portion of each tuple and persist it memory for later use
   // val ticks_min30 = ticks.map(record => (convert_to_30min(record._1),
   //                                        record._2,
   //                                        record._3)).persist

   // // compute the average price for each 30 minute period
   // val price_min30 = ticks_min30.map(record => (record._1, (record._2, 1)))
   //                              .reduceByKey( (x, y) => (x._1 + y._1,
   //                                                       x._2 + y._2) )
   //                              .map(record => (record._1,
   //                                              record._2._1/record._2._2) )

   // // compute the total volume for each 30 minute period
   // val vol_min30 = ticks_min30.map(record => (record._1, record._3))
   //                            .reduceByKey(_+_)

   // // join the two RDDs into a new RDD containing tuples of (30 minute time periods, average price, total volume)
   // val price_vol_min30 = price_min30.join(vol_min30)
   //                                  .sortByKey()
   //                                  .map(record => (record._1,
   //                                                  record._2._1,
   //                                                  record._2._2))

   // // save the data back into HDFS
   // price_vol_min30.saveAsTextFile("hdfs://<public_dns>:9000/user/price_data_output_scala")
 }
}