class agg_union():

  def __init__(self, df_name="", groups=[], cols=[], agg_funcs=[]):
    
    """
      df_name:   type string, the name of the df you are passing to be grouped
           ex:   'df_active_users_grouped'
    
       groups:   type list, integer representation of column indexing (+1) of the grouping to take place
           ex:   [123, 21] -> [[cols[0], cols[1], cols[2]], [cols[1], cols[0]]]
           ex:   [[1,2,3], [2,1]]  -> [[cols[0], cols[1], cols[2]], [cols[1], cols[0]]]
    
         cols:   type list, columns of df that are to be grouped
           ex:   ["year", "month", "day", "country", "devicecategory"]
      
    agg_funcs:   type list (multiple aggregations) or string (single aggregation), aggregation function to be used with columns to be aggregated
           ex:   ['F.countDistinct(F.col("fullvisitorid")), F.countDistinct("fullvisitorid","visitid")']
           ex:   'F.countDistinct(F.col("fullvisitorid"))
    """
    
    self.df = df_name
    self.groups = groups
    self.cols = cols    
    self.agg_funcs = agg_funcs

    # dict -> keys: column groupings name, values: columns to group by 
    group_dict = {}
    # split int or list representations of grouping variables into column groupings 
    #    [123, 21]                   -> [[cols[0], cols[1], cols[2]], [cols[1], cols[0]]]
    #    [[[1],[2],[3]], [[2],[1]]]  -> [[cols[0], cols[1], cols[2]], [cols[1], cols[0]]]
    for grp in self.groups:
      if isinstance(grp, int):
        colgrp = [self.cols[int(i)-1] for i in str(grp)]
      elif isinstance(grp, list):
        colgrp = [self.cols[int(i)-1] for i in grp]      
      k = "_".join(_ for _ in colgrp).lower()
      # list of columns in form 'F.col(column)'
      v0 = ['F.col("{}")'.format(_) for _ in colgrp]
      # list of columns
      v1 = [_ for _ in colgrp]
      group_dict[k] = [v0,v1]
    self.group_dict = group_dict
    
  def print_groups(self):
    return self.group_dict
  
  def print_columns(self):
    return self.cols
  
  def add_groupby(self):
    gb = '{}.groupby({})'
    gbs = {}
    
    for k in self.group_dict:
      s = ",".join(self.group_dict[k][0])
      gbs[k] = gb.format(self.df, s)
     
    return gbs
      
  def add_aggfunc(self):
    agg_exp = '.agg({})'
    afs = {}

    for k in self.group_dict:
      if isinstance(self.agg_funcs, str):
        afs[k] = agg_exp.format(self.agg_funcs)
      elif isinstance(self.agg_funcs, list):
        agg_str = ""
        for f in self.agg_funcs:
          agg_str += "{},".format(f)
        afs[k] = agg_exp.format(agg_str)

    return afs
    
  def add_na(self):
    wc = '.withColumn("{}", F.lit("(All {})"))'
    nas = {}

    for k in self.group_dict:
      s = ""
      for col in self.cols:
        if col not in self.group_dict[k][1]:
          s += wc.format(col, col)
      nas[k] = s
    
    return nas
  
  def add_group_names(self):
    wc = '.withColumn("grouping", F.lit("{}"))'
    gn = {}
    
    for k in self.group_dict:
      gn[k] = wc.format(k)
    
    return gn

  def generate_string(self):
    li_dicts = [self.add_groupby(), self.add_aggfunc(), self.add_group_names(), self.add_na()]
    union = ".unionByName({})"
    s = ""
    
    for idx, grouping in enumerate(self.group_dict):
      df = ""
      for d in li_dicts:
        for k in d:
          if k == grouping:
            df += d[k]
      if idx == 0:
        s += df
      else:
        s += union.format(df)
    
    return s

  def evaluate(self):
    s = self.generate_string()
    return eval(s)