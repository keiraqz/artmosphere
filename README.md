#Artmosphere

<img src="https://github.com/keiraqz/artmosphere/blob/master/img/cover.png" alt="alt text" width="600" height="350">

<!--Website: <a href="http://www.artmosphere.nyc"  target="_blank">www.artmosphere.nyc</a>-->

*Note: The original website is down at the termination of the Insight program. However, the video demo of the website is available <a href="https://youtu.be/skzZ7sosC8c"  target="_blank">here</a>. Slides are available <a href= "http://www.slideshare.net/KeiraZhou2/artmosphere-demo" target="_blank">here</a>.*

Code for the web framework Flask can be found <a href="https://github.com/keiraqz/artmosphere/blob/master/flask/app/views.py"  target="_blank">here</a>. Code for front end web application can be found in <a href="https://github.com/keiraqz/artmosphere/tree/master/flask/app/templates"  target="_blank">this folder</a>. 


##Table of Contents
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#introduction">Introduction</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#settings">Settings</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#data-processing">Data Processing</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#website">Website</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#presentation-deck">Presentation Deck</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#packages-used-for-the-pipeline">Packages Used for the Pipeline</a>


##Introduction
This is a data engineering project at <a href= "http://insightdataengineering.com/" target="_blank">Insight Data Engineering Fellow Program</a>. The project provides a platform for users to search for different artworks, see similar art pieces and real-time popularity of a given art piece. Users can also see where all the artworks have been uploaded across the world. The main goal of the program to learn different tools used in a data pipeline for processing large datasets in a distributed manner.


**Tools used:**
- Data ingestion: <a href= "http://kafka.apache.org/" target="_blank">Kafka</a>
- Data storage: <a href= "https://hadoop.apache.org/" target="_blank">Hadoop Distributed File System</a>
- Batch processing: <a href= "https://spark.apache.org/" target="_blank">Spark</a>
- Real-time processing: <a href= "https://spark.apache.org/streaming/" target="_blank">Spark Streaming</a>
- Database: <a href= "https://www.elastic.co/products/elasticsearch" target="_blank">Elasticsearch</a>, <a href= "http://cassandra.apache.org/" target="_blank">Cassandra</a>
- Web API: <a href= "http://flask.pocoo.org/" target="_blank">Flask</a>
- Website: <a href= "http://getbootstrap.com/" target="_blank">Bootstrap</a>, <a href= "http://www.highcharts.com/" target="_blank">Highcharts</a>


##Settings
**Dataset:**
The dataset is a collection of 26,000 artworks and 45,000 artists collected from <a href= "https://www.artsy.net/" target="_blank">Artsy.net</a> in JSON format. In order to simulate real-time user activities, the project also used self-engineered data in two formats:
- Collecting log: timestamp, user\_id, collected, artwork\_id
- Uploading log: timestamp, user\_id, uploaded, artwork\_id, location\_code


**AWS Clusters:**
A distributed AWS cluster of 4 EC2 machines is being used for this project. All the components (ingestion, batch and real-time processing) are configured and run in distributed mode, with 1 master node and 3 slave nodes. The master node has 8GB of memory and 50GB of storage. The work nodes each has 8GB of memory and 1TB of storage.


##Data Processing
<img src="https://github.com/keiraqz/artmosphere/blob/master/img/pipeline.png" alt="alt text" width="600" height="300">

- **Data Ingestion (Kafka):** The datasets for batch and real-time processing are ingested using Kafka. For batch processing, the datasets are stored into HDFS. For real-time processing, the data is streamed into Spark Streaming.
  - Streaming producer: <a href= "https://github.com/keiraqz/artmosphere/blob/master/kafka/my_streaming_producer.py" target="_blank">my\_streaming\_producer.py</a>
  - Batch producer: <a href= "https://github.com/keiraqz/artmosphere/blob/master/kafka/hdfs_producer.py" target="_blank">hdfs\_producer.py</a>
  - Batch consumer: <a href= "https://github.com/keiraqz/artmosphere/blob/master/kafka/hdfs_consumer.py" target="_blank">hdfs\_consumer.py</a>

- **Batch Processing (HDFS, Spark):** To perform batch processing job, Spark loads the data from HDFS and processed them in a distributed way. The two major batch processing steps for the project is to aggregate the artists upload locations and compute artwork-artwrok similarties. 
  - Aggreate Locations: <a href= "https://github.com/keiraqz/artmosphere/tree/master/batch_geo" target="_blank">batch\_geo</a>
    - To excute: run ```bash batch_geo_run.sh```
  - Compute Similarity: <a href= "https://github.com/keiraqz/artmosphere/blob/master/batch_similarity/compute_similarity.py" target="_blank">compute\_similarity.py</a>
    - To excute: run ```bash batch_sim_run.sh```
  
  The following graph shows the performance analysis of Spark for one the batch processing jobs - aggregating artists upload locations - up to 500GB:

  <img src="https://github.com/keiraqz/artmosphere/blob/master/img/Spark.png" alt="alt text" width="600">

- **Serving Layer (Elasticsearch, Cassandra):** The platform provides a search function that searches a given keyword within the artworks' title. In order to achieve this goal, the metadata of all artworks are stored into Elasticsearch. All artworks and artists are stored in Cassandra tables and can be retrieved by ids. The aggregated artists locations are also stored in Cassandra table, which can be queried by location\_code and timestamp.

- **Stream Processing (Spark Streaming):** Spark Streaming processes the data in micro batches. The job aggregates how many people collected a certain piece of art every 5 seconds and saves the result into a table in Cassandra. The information can be queried by artwork\_id and timestamp.
  - Streaming Processing: <a href= "https://github.com/keiraqz/artmosphere/tree/master/spark_streaming" target="_blank">spark\_streaming</a>
    - To excute: run ```bash log_streaming_run.sh```

- **Front-end (Flask, Bootstrap, Highcharts):** The frond-end uses Flask as the framework and the website uses JavaScript and Twitter Bootstrap libriries. All the plots are achieved via Highcharts. To visit: <a href="http://www.artmosphere.nyc"  target="_blank">www.artmosphere.nyc</a>


##Website
*Note: Website is down at the termination of the Insight program. However, the video demo of the website is available <a href="https://youtu.be/skzZ7sosC8c"  target="_blank">here</a>.*

<!--<a href="http://www.artmosphere.nyc"  target="_blank">www.artmosphere.nyc</a>-->
- The artwork information:

<img src="https://github.com/keiraqz/artmosphere/blob/master/img/art_info.png" alt="alt text" width="600">

- Display similar artworks:

<img src="https://github.com/keiraqz/artmosphere/blob/master/img/similar.png" alt="alt text" width="200">

- Plots show in real-time how many people have collected this piece of art within a 5-sec frame:

<img src="https://github.com/keiraqz/artmosphere/blob/master/img/trend.png" alt="alt text" width="300">
<img src="https://github.com/keiraqz/artmosphere/blob/master/img/trend2.png" alt="alt text" width="300">

- A map shows where all the artworks have been uploaded across the world:

<img src="https://github.com/keiraqz/artmosphere/blob/master/img/map.png" alt="alt text" width="600">

##Presentation Deck
The presentation slides are available <a href= "http://www.slideshare.net/KeiraZhou2/artmosphere-demo" target="_blank">here</a>.

The video demo of the website is available <a href="https://youtu.be/skzZ7sosC8c"  target="_blank">here</a>.

##Packages Used for the Pipeline
pyspark, pyspark-cassandra, elasticsearch-hadoop-2.1.0.Beta2.jar


