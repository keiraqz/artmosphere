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
import org.apache.spark.mllib.linalg.distributed.RowMatrix
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.param.ParamMap
import org.apache.spark.mllib.linalg.{Vector, Vectors}
import org.apache.spark.mllib.regression.LabeledPoint

// import datetime

object ArtSimilarity {
  def main(args: Array[String]) {

    val brokers = "ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9092"
    val topics = "user_activity"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("art_data").set("spark.cassandra.connection.host", "172.31.11.233")
    
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)
    import sqlContext._



    val filename = "hdfs://ec2-54-183-55-185.us-west-1.compute.amazonaws.com:9000/insight/artsy/engr_gene/a5000_g20.json"

    // Load and parse the data file.
    val rows = sc.textFile(filename).map { line =>
      val values = line.split(' ').map(_.toDouble)
      Vectors.dense(values)
    }
    val mat = new RowMatrix(rows)

    // Compute similar columns perfectly, with brute force.
    val simsPerfect = mat.columnSimilarities()


  }
}