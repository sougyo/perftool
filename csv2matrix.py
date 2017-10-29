#!/usr/bin/env python

import collections
import csv
import sys

d = {}
key_list  = collections.OrderedDict()
time_list = collections.OrderedDict()
prev_time = None
cnt = 0

for (time, k1, k2, val) in csv.reader(sys.stdin):
  if time != prev_time:
    cnt += 1

  if not val:
    continue

  internal_time = (cnt, time)

  key = "{}-{}".format(k1, k2)
  if not d.has_key(internal_time):
    d[internal_time] = {}
  d[internal_time][key] = val

  time_list[internal_time] = True
  key_list[key]            = True

  prev_time = time


writer = csv.writer(sys.stdout)
writer.writerow(["time"] + key_list.keys())
for internal_time in time_list:
  (cnt, time) = internal_time
  writer.writerow([time] + [d[internal_time].get(key) for key in key_list])
