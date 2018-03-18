#!/usr/bin/env python

import collections
import csv
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--prefix' , type=str, help='prefix_key')
parser.add_argument('--postfix', type=str, help='postfix_key')
args = parser.parse_args()

d = {}
key_list  = collections.OrderedDict()
time_list = collections.OrderedDict()
prev_time = None
cnt = 0

for (time, k1, k2, val) in csv.reader(sys.stdin):
  if time != prev_time:
    cnt += 1

  internal_time = (cnt, time)

  key = str(k1)
  if k2:
   key += "." + str(k2)

  if not (internal_time in d):
    d[internal_time] = {}

  d[internal_time][key] = val

  time_list[internal_time] = True
  key_list[key]            = True

  prev_time = time

column_names = key_list.keys()
if args.prefix:
  column_names = [("%s%s" % (args.prefix, k))  for k in column_names]
if args.postfix:
  column_names = [("%s%s" % (k, args.postfix)) for k in column_names]

writer = csv.writer(sys.stdout)
writer.writerow(["time"] + list(column_names))
for internal_time in time_list:
  (cnt, time) = internal_time
  writer.writerow([time] + [d[internal_time].get(key) for key in key_list])
