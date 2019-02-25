#!/usr/bin/env python

import sys
import csv
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

parser = argparse.ArgumentParser(description='random forest')
parser.add_argument('-i', '--index_name', type=str, help='index name')
parser.add_argument('--top_n', type=int, help='show only top n result')
parser.add_argument('--plot', action='store_true')
parser.add_argument('filepath', nargs=1)
parser.add_argument('column'  , nargs=1)
args = parser.parse_args()

df = pd.read_csv(args.filepath[0],
        index_col=(args.index_name or 'time')).fillna(0)
df = df.loc[:, df.var() != 0]

target_column = args.column[0]
columns = list(df.columns)

if columns.count(target_column) != 1:
  print("'{}' is not found or is duplicated in columns".format(target_column))
  sys.exit(1)

columns.remove(target_column)
rf = RandomForestRegressor()
rf.fit(df[columns], df[target_column])

vals, labels = map(list, zip(*(sorted(zip(rf.feature_importances_, columns)))))

if args.top_n:
  vals = vals[len(vals)-args.top_n:]
  labels = labels[len(labels)-args.top_n:]

writer = csv.writer(sys.stdout)
for (v, l) in reversed(list(zip(vals, labels))):
  writer.writerow([l, v])

if args.plot:
  import matplotlib.pyplot as plt
  data_range = range(len(vals))
  plt.barh(data_range, vals, align='center')
  plt.yticks(data_range, labels)
  plt.title(target_column)
  plt.show()
