#!/usr/bin/env python

import csv
import sys

prev = None
l = []
writer = csv.writer(sys.stdout)

for (time, k1, k2, val) in csv.reader(sys.stdin):
  if not val:
    continue

  current = [time, k2]

  if current != prev and l:
    writer.writerow(prev + l)
    l = []

  l.extend([k1, val])
  prev = current

if l:
  writer.writerow(prev + l)
