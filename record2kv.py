#!/usr/bin/env python

import csv
import sys

writer = csv.writer(sys.stdout)
for a in csv.reader(sys.stdin):
  time = a.pop(0)
  k2   = a.pop(0)

  while a:
    k1  = a.pop(0)
    val = a.pop(0)

    writer.writerow([time, k1, k2 or None, val])
