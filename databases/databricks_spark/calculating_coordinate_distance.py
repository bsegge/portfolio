# DBTITLE 1,Import needed modules
import math


# DBTITLE 1,Create directory and move files
assgn_dir = "FileStore/tables/geoData"
base_dir = "FileStore/tables/"
files = ["geoPoints0.csv","geoPoints1.csv"]

dbutils.fs.mkdirs(assgn_dir)
sc = spark.sparkContext

for f in files:
  cur_dir = base_dir + f
  dbutils.fs.cp(cur_dir, assgn_dir)


# DBTITLE 1,Read files and create df
txt_files = ["dbfs:///FileStore/tables/geoData/" + i for i in files]

url_tuples = []
for f in txt_files:
  file = sc.textFile(f)
  out = file.map(lambda line: (line.split(",")))
  url_tuples.append(out.collect())
  
li_pts = sc.parallelize(url_tuples).flatMap(lambda x: x)

print(li_pts.collect())


# DBTITLE 1,Variable to hold list of distances
distances = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]


# DBTITLE 1,Creating the grids for each distance (persisted b/c used multiple times)
gridRDD = li_pts.flatMap(
  lambda x: [(f'dist: {dist}', (x[0], (math.floor(float(x[1])/dist), math.floor(float(x[2])/dist)), (x[1],x[2]))) for dist in distances]
)

gridRDD.persist()


# DBTITLE 1,The "real" grid positions (not those below or to the right)
dist_pts = [(f'{dist}', gridRDD.filter(lambda x: x[0] == f'dist: {dist}').map(lambda x: (x[1][1], x[1][2])).collect()) for dist in distances]


# DBTITLE 1,"Placing" values in grid spaces below and to the right
belowRDD = gridRDD.map(lambda x: [(x[0], (x[1][0] , (x[1][1][0] - i, x[1][1][1] - 1), x[1][2])) for i in range(1, -2, -1)]).flatMap(lambda x: x)
rightRDD = gridRDD.map(lambda x: (x[0], (x[1][0] , (x[1][1][0] + 1, x[1][1][1]), x[1][2])))


# DBTITLE 1,Bringing it all together
unionedRDD = gridRDD.union(rightRDD).union(belowRDD)


# DBTITLE 1,combineByKey function building
# if the value is in the list of "real" grid locations, and it isn't equal to itself, add the sorted tuple pair
def cc(value):
  out = []
  for idx, val in enumerate(cur_dist_pt[1]):
    if value[1] == val[0] and value[0] != f'Pt{idx:02}':
      out.append((sorted((value[0], f'Pt{idx:02}')), (value[2], val[1])))
  return out

# same as above
def mv(prev, value):
  for idx, val in enumerate(cur_dist_pt[1]):
    if value[1] == val[0] and value[0] != f'Pt{idx:02}':
      prev.append((sorted((value[0], f'Pt{idx:02}')), (value[2], val[1]))  )  
  return prev

# not really needed
def mc(prev1, prev2):       
  prev1.extend(prev2)    
  return prev1


# DBTITLE 1,Function to measure distance between coordinates
def cord_distance(x):
  dist_set = set()
  thresh = float(x[0].split(" ")[-1])
  for _ in x[1]:
    dist = (tuple(_[0]), math.sqrt((float(_[1][0][0])-float(_[1][1][0]))**2 + (float(_[1][0][1])-float(_[1][1][1]))**2))
    if dist[1] <= thresh:
      dist_set.add(dist)
  return dist_set


# DBTITLE 1,Looping through distances, splitting my RDD's accordingly, and printing results
list_pairs = []
for dist in distances:
  # for use in combineByKey
  cur_dist_pt = dist_pts.pop(0)
  # filter RDD for current distance calculation
  cur_rdd = unionedRDD.filter(lambda x: x[0] == f'dist: {dist}')
  # combine by definitions above
  cur_rdd = cur_rdd.combineByKey(cc, mv, mc).sortByKey()
  # measure distance and keep those that are within the bounds
  cur_rdd = cur_rdd.map(lambda x: (x[0], cord_distance(x))).collect()
  print(f'Dist: {cur_rdd[0][0].split(" ")[-1]}, Num pairs: {len(cur_rdd[0][1])}', cur_rdd[0][1], "\n")



