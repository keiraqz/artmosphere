import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.sql._
import com.datastax.spark.connector._
import com.datastax.spark.connector.cql.{ColumnDef, RegularColumn, TableDef}
import com.datastax.spark.connector.types.IntType
import com.datastax.spark.connector.writer._
import org.apache.cassandra.serializers.TimestampSerializer
import java.util.Date
import org.joda.time.DateTime
import org.joda.time.format.DateTimeFormat


object GeoData {
  def main(args: Array[String]) {

    val sparkConf = new SparkConf().setAppName("geo_data").set("spark.cassandra.connection.host", "172.31.11.232")
    val sc = new SparkContext(sparkConf)
    val path = "hdfs://ec2-54-215-136-187.us-west-1.compute.amazonaws.com:9000/insight/artsy/geo*"
    val distFile = sc.textFile(path)
    val format = new java.text.SimpleDateFormat("yyyy-mm-dd")
    val sqlContext = SQLContextSingleton.getInstance(sc)
    import sqlContext.implicits._
    val current_time = TimestampFormatter.format(new Date())

    val ticksDF = distFile.map( x => {
                                  val tokens = x.split(";")
                                  Post(tokens(0), tokens(1))
                                  }).toDF()
    val ticks_per_source_DF = ticksDF.groupBy("code").count().collect()
    var ticks_with_time = ticks_per_source_DF.map(x => (current_time,x(0),x(1)))
    sc.parallelize(ticks_with_time).saveToCassandra("art_pin_log", "art_geo_count", SomeColumns("event_time","code","count"))
  }
}

case class Post(location: String, code: String)

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

  private val TimestampPattern = "yyyy-MM-dd"

  def format(date: Date): String =
    DateTimeFormat.forPattern(TimestampPattern).print(new DateTime(date.getTime))
}
