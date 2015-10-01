#Artmosphere
Website: www.artmosphere.nyc

<img src="https://github.com/keiraqz/artmosphere/blob/master/img/cover.png" alt="alt text" width="600" height="350">


##Table of Contents
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#introduction">Introduction</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#settings">Settings</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#data-processing">Data Processing</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#website">Website</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#presentation-deck">Presentation Deck</a>
- <a href= "https://github.com/keiraqz/artmosphere/blob/master/README.md#packages-used-for-the-pipeline">Packages Used for the Pipeline</a>


##Introduction
This is a data engineering project at <a href= "http://insightdataengineering.com/">Insight Data Engineering Fellow Program</a>. The project provides a platform for users to search for different artworks, see similar art pieces and real-time popularity of a given art piece. Users can also see where all the artworks have been uploaded across the world. The main goal of the program to learn different tools used in a data pipeline for processing large datasets in a distributed manner.


**Tools used:**
- Data ingestion: <a href= "http://kafka.apache.org/">Kafka</a>
- Data storage: <a href= "https://hadoop.apache.org/">Hadoop Distributed File System</a>
- Batch processing: <a href= "https://spark.apache.org/">Spark</a>
- Real-time processing: <a href= "https://spark.apache.org/streaming/">Spark Streaming</a>
- Database: <a href= "https://www.elastic.co/products/elasticsearch">Elasticsearch</a>, <a href= "http://cassandra.apache.org/">Cassandra</a>
- Web API: <a href= "http://flask.pocoo.org/">Flask</a>
- Website: <a href= "http://getbootstrap.com/">Bootstrap</a>, <a href= "http://www.highcharts.com/">Highcharts</a>


##Settings
**Dataset:**
The dataset is a collection of 26,000 artworks and 45,000 artists collected from <a href= "https://www.artsy.net/">Artsy.net</a> in JSON format. In order to simulate real-time user activities, the project also used self-engineered data in two formats:
- Collecting log: timestamp, user\_id, collected, artwork\_id
- Uploading log: timestamp, user\_id, uploaded, artwork\_id, location\_code


**AWS Clusters:**
A distributed AWS cluster of 4 EC2 machines is being used for this project. All the components (ingestion, batch and real-time processing) are configured and run in distributed mode, with 1 master node and 3 slave nodes. The master node has 8GB of memory and 50GB of storage. The work nodes each has 8GB of memory and 1TB of storage.


##Data Processing
<img src="https://github.com/keiraqz/artmosphere/blob/master/img/pipeline.png" alt="alt text" width="600" height="300">

- **Data Ingestion (Kafka):** The datasets for batch and real-time processing are ingested using Kafka. For batch processing, the datasets are stored into HDFS. For real-time processing, the data is streamed into Spark Streaming.
  - Streaming producer: <a href= "https://github.com/keiraqz/artmosphere/blob/master/kafka/my\_streaming\_producer.py">my\_streaming\_producer.py</a>
  - Batch producer: <a href= "https://github.com/keiraqz/artmosphere/blob/master/kafka/hdfs\_producer.py">hdfs\_producer.py</a>
  - Batch consumer: <a href= "https://github.com/keiraqz/artmosphere/blob/master/kafka/hdfs\_consumer.py">hdfs\_consumer.py</a>

- **Batch Processing (HDFS, Spark):** To perform batch processing job, Spark loads the data from HDFS and processed them in a distributed way. The two major batch processing steps for the project is to aggregate the artists upload locations and compute artwork-artwrok similarties. 
  - Aggreate Locations: <a href= "https://github.com/keiraqz/artmosphere/tree/master/batch\_geo">batch\_geo</a>
    - To excute: run ```bash batch_geo_run.sh```
  - Compute Similarity: <a href= "https://github.com/keiraqz/artmosphere/tree/master/batch\_similarity">batch\_similarity</a>
    - To excute: run ```bash batch_sim_run.sh```
  
  The following graph shows the performance analysis of Spark for one the batch processing jobs - aggregating artists upload locations - up to 500GB:

  <img src="https://github.com/keiraqz/artmosphere/blob/master/img/Spark.png" alt="alt text" width="600">

- **Serving Layer (Elasticsearch, Cassandra):** The platform provides a search function that searches a given keyword within the artworks' title. In order to achieve this goal, the metadata of all artworks are stored into Elasticsearch. All artworks and artists are stored in Cassandra tables and can be retrieved by ids. The aggregated artists locations are also stored in Cassandra table, which can be queried by location\_code and timestamp.

- **Speed Layer (Spark Streaming):** Spark Streaming processes the data in micro batches. The job aggregates how many people collected a certain piece of art every 5 seconds and saves the result into a table in Cassandra. The information can be queried by artwork\_id and timestamp.
  - Streaming Processing: <a href= "https://github.com/keiraqz/artmosphere/tree/master/spark\_streaming</a>
    - To excute: run ```bash log_streaming_run.sh```

- **Front-end (Flask, Bootstrap, Highcharts):** The frond-end uses Flask as the framework and the website uses JavaScript and Twitter Bootstrap libriries. All the plots are achieved via Highcharts. To visit: www.artmosphere.nyc


##Website
www.artmosphere.nyc
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
The presentation slides are available <a href= "http://www.artmosphere.nyc/slide">here</a>.

##Packages Used for the Pipeline
pyspark, pyspark-cassandra, elasticsearch-hadoop-2.1.0.Beta2.jar


