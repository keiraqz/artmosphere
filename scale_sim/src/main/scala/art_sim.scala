import kafka.serializer.StringDecoder
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}
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
import org.apache.spark.mllib.linalg.distributed.{MatrixEntry, RowMatrix}
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.mllib.linalg.{Vector, Vectors}
import org.apache.spark.mllib.regression.LabeledPoint
// import scopt.OptionParser
// import datetime

object ArtSimilarity {
  def main(args: Array[String]) {

    val brokers = "ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9092"
    val topics = "user_activity"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("art_data").set("spark.cassandra.connection.host", "172.31.11.233")
    
    val sc = new SparkContext(sparkConf)
    val sqlContext = new SQLContext(sc)
    import sqlContext._



    val filename = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/engr_gene/a500000_g1000_bit.txt"

    val current_time_1 = new Date()
    // Load and parse the data file.
    val rows = sc.textFile(filename).map { line =>
      val values = line.split(' ').map(_.toDouble)
      Vectors.dense(values)
    }
    
    val mat = new RowMatrix(rows)
    // val current_time_1 = new Date()
    // Compute similar columns perfectly, with brute force.
    val exact = mat.columnSimilarities()
    // val current_time_2 = new Date()
    // Compute similar columns with estimation using DIMSUM
    val approx = mat.columnSimilarities(0.1) // a threshold
    // val current_time_2 = new Date()

    val exactEntries = simsPerfect.entries.map { case MatrixEntry(i, j, u) => ((i, j), u) }
    val approxEntries = approx.entries.map { case MatrixEntry(i, j, v) => ((i, j), v) }

    val MAE = exactEntries.leftOuterJoin(approxEntries).values.map {
      case (u, Some(v)) =>
        math.abs(u - v)
      case (u, None) =>
        math.abs(u)
    }.mean()

    println(s"Average absolute error in estimate is: $MAE")

    sc.stop()

  }
}