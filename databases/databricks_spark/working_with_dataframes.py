from pyspark.sql import Row
from pyspark.sql import functions as f
from pyspark.sql.types import StructType, StructField, LongType, StringType

sc = spark.sparkContext

baseballFile = "FileStore/tables/Master.csv"
bballRDD = sc.textFile(baseballFile).map(lambda x: x.split(","))
bballRDD = bballRDD.map(lambda x: filter(lambda x: x != ""))

bballSchema = (
  StructType(                        
    [
      StructField('playerID', StringType(), True),                          
      StructField('birthCountry', StringType(), True),                           
      StructField('birthState', StringType(), True),                            
      StructField('height', StringType(), True)
    ]
  )
)

bballRowsRdd = (
  bbRDD.map(
    lambda x:
    Row(
      playerID = x[0],
      birthCountry = x[4],
      birthState = x[5],
      height = x[17]
    )
  )
)


bbDF = spark.createDataFrame(bballRowsRdd, bballSchema)
bbDF = bbDF.filter(bbDF.playerID != "playerID")


bbDF.createOrReplaceTempView("bball")
spark.sql("SELECT count(distinct playerID) as count_players FROM bball WHERE bball.birthState = 'CO'").show()


bbDF.where(bbDF.birthState == "CO").select("playerID").distinct().count()


spark.sql("SELECT birthCountry, round(avg(height),2) as avg_height FROM bball GROUP BY birthCountry ORDER BY 2 DESC").show(bbDF.count())

(
  bbDF.select(bbDF.birthCountry,bbDF.height)
  .groupby(bbDF.birthCountry)
  .agg({"height":"mean"})
  .withColumnRenamed("avg(height)", "avg_height")
  .withColumn("avg_height", f.round("avg_height", 2))
  .orderBy("avg_height", ascending = False)
  .show(bbDF.count())
)
