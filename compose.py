#!/usr/bin/env python

import csv
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--prefix_key' , type=str, help="specify a key used as prefix")
args = parser.parse_args()

prev = None
l = []
writer = csv.writer(sys.stdout)

prefix_dict = {}

def write_prev_row():
  if l:
    time = prev[0]
    k2   = prev[1]
    if k2 in prefix_dict:
      k2 = prefix_dict[k2] + k2
    writer.writerow([time, k2] + l)

for (time, k1, k2, val) in csv.reader(sys.stdin):
  if not val:
    continue

  if k1 == args.prefix_key:
    prefix_dict[k2] = prefix_dict.get(k2) or (val + "-")

  current = [time, k2]

  if current != prev:
    write_prev_row()
    l = []

  l.extend([k1, val])
  prev = current

write_prev_row()
