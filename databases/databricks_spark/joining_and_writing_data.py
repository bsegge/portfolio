from pyspark.sql import functions as f, Window as w


# allstar dataframe
allstar = "FileStore/tables/AllstarFull.csv"
allstarDF = spark.read.format("csv").option("header", True).option("inferSchema", True).load(allstar)
allstarDF = allstarDF.select("playerID","teamID")

# team dataframe
team = "FileStore/tables/Teams.csv"
teamDF = spark.read.format("csv").option("header", True).option("inferSchema", True).load(team)
teamDF = teamDF.select("teamID", "name")

# master dataframe
master = "FileStore/tables/Master.csv"
masterDF = spark.read.format("csv").option("header", True).option("inferSchema", True).load(master)
masterDF = masterDF.select("playerID","nameFirst","nameLast")


masterDF.show()


joinedDF = (
  allstarDF.join(teamDF, "teamID")
  .join(masterDF, "playerID")
  .distinct()
  .withColumnRenamed("name","teamName")
)


joinedDF.show()


joinedDF.write.format("parquet").partitionBy("teamName").mode("overwrite").save("FileStore/tables/lab6df")


temp = "FileStore/tables/lab6df"
tempDF = spark.read.format("parquet").option("header", True).option("inferSchema", True).load(temp)
display(tempDF)


# create window function for later count
window = w.partitionBy("teamName").rowsBetween(w.unboundedPreceding, w.unboundedFollowing)

display(
  tempDF.filter(tempDF.teamName == "Colorado Rockies")
  .withColumn("cnt_players",f.count(f.lit(1)).over(window))
)


rockies = (
  tempDF.filter(tempDF.teamName == "Colorado Rockies")
  .withColumn("cnt_players",f.count(f.lit(1)).over(window))
)
rockies.show(rockies.count())



