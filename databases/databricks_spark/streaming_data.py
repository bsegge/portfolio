# Data file too large to store on Git


from pyspark.sql.types import StructType, StructField, LongType, StringType, DoubleType, TimestampType
from pyspark.sql import functions as f


# DBTITLE 1,Original File Directory
fifa = "FileStore/tables/FIFA.csv"


# DBTITLE 1,Schema
fifaSchema = StructType( \
                        [StructField('ID', LongType(), True), \
                         StructField('lang', StringType(), True), \
                         StructField('Date', TimestampType(), True), \
                         StructField('Source', StringType(), True), \
                         StructField('len', LongType(), True), \
                         StructField('Orig_Tweet', StringType(), True), \
                         StructField('Tweet', StringType(), True), \
                         StructField('Likes', LongType(), True), \
                         StructField('RTs', LongType(), True), \
                         StructField('Hashtags', StringType(), True), \
                         StructField('UserMentionNames', StringType(), True), \
                         StructField('UserMentionID', StringType(), True), \
                         StructField('Name', StringType(), True), \
                         StructField('Place', StringType(), True), \
                         StructField('Followers', LongType(), True), \
                         StructField('Friends', LongType(), True), \
                        ])


# DBTITLE 1,Read Original
df_fifa = spark.read.format("csv").option("header", True).schema(fifaSchema).option("mode", "dropMalformed").load(fifa)


display(df_fifa)


# DBTITLE 1,Repartition and Persist
df_fifa = df_fifa.repartition(15).orderBy(f.col('Date')).persist()


# DBTITLE 1,Remove NULL Hashtags
df_fifa = df_fifa.select(f.col("ID"),f.col("Date"),f.col("Hashtags")).where(~f.isnull("Hashtags"))


# DBTITLE 1,Explode
df_fifa = df_fifa.withColumn("Hashtags", f.explode(f.split(f.col("Hashtags"),",")))


display(df_fifa)


# DBTITLE 1,Static Window Query
staticWin = (
  df_fifa.groupBy([f.window("Date", "60 minutes", "30 minutes"), f.col("Hashtags")])
  .agg(f.count(f.col("ID")).alias("count_tweets"))
  .where(f.col("count_tweets") > 100)
)


# staticWin.orderBy("Window").show(20, staticWin.count(), False)
staticWin.orderBy("Window").show(20, False)


# DBTITLE 1,Write Small Files to Directory
lab7_dir = "FileStore/tables/lab7"
df_fifa.write.format("csv").option("header", True).save(lab7_dir)


# DBTITLE 1,Stream Schema
streamSchema = StructType( \
                        [StructField('ID', LongType(), True), \
                         StructField('Date', TimestampType(), True), \
                         StructField('Hashtags', StringType(), True), \
                        ])


# dbutils.fs.rm("local_disk0", True)


# DBTITLE 1,Stream Source
sourceStream = (
  spark.readStream.format("csv")
  .option("header", True)
  .schema(streamSchema)
  .option("maxFilesPerTrigger", 1)
  .load("dbfs:///"+lab7_dir)
)


# DBTITLE 1,Stream Query
tweetCountWin = (
  sourceStream.withWatermark("Date", "24 hours")
  .groupBy([f.window(f.col("Date"), "60 minutes", "30 minutes"), f.col("Hashtags")])
  .agg(f.count(f.col("ID")).alias("tweet_count"))
  .where(f.col("tweet_count") > 100)
)


# DBTITLE 1,Start Stream
sinkStream = tweetCountWin.writeStream.outputMode("complete").format("memory").queryName("tweetWin").start()


# DBTITLE 1,Query Stream Data
cur = spark.sql("SELECT * FROM tweetWin WHERE tweet_count > 100")
cur.show(20, False)



