#!/usr/bin/env python

import collections
import csv
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--default', type=float, help='default value of N/A')
args = parser.parse_args()

d = {}
key_list  = collections.OrderedDict()
time_list = collections.OrderedDict()
prev_time = None
cnt = 0

for a in csv.reader(sys.stdin):
  if len(a) == 0:
    continue

  time, k1, k2, val = a

  if time != prev_time:
    cnt += 1

  cnt_time = (cnt, time)

  key = str(k1)
  if k2:
   key += "." + str(k2)

  if not (cnt_time in d):
    d[cnt_time] = {}

  d[cnt_time][key] = val

  time_list[cnt_time] = True
  key_list[key]       = True

  prev_time = time

def val_or_default(v):
  if (v is None) and (args.default is not None):
    return args.default
  return v

writer = csv.writer(sys.stdout)
writer.writerow(["time"] + list(key_list.keys()))
for cnt_time in time_list:
  (cnt, time) = cnt_time
  writer.writerow([time] + [val_or_default(d[cnt_time].get(key)) for key in key_list])
