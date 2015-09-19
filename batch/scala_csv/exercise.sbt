name := "load_csv"

version := "1.0"

scalaVersion := "2.10.4"

libraryDependencies ++= Seq(
"org.apache.spark" %% "spark-core" % "1.4.1" % "provided",
"org.elasticsearch" %% "elasticsearch-spark % "0.19.8"
)
