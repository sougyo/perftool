#!/usr/bin/env python

import sys
import argparse
import csv
import re

parser = argparse.ArgumentParser(description='unit converter')
parser.add_argument('-i', action='store_true', help='KiB, MiB, GiB,...')
parser.add_argument('-o', type=str, help='output unit')
args = parser.parse_args()

k = 1024 if args.i else 1000
coef = { 'k': k ** 1,
         'm': k ** 2,
         'g': k ** 3,
         't': k ** 4,
         'p': k ** 5, }

def conv(val, unit):
  val *= coef[unit.lower()]
  if args.o:
    val /= (coef.get(args.o.lower()) or 1)
  return val 

unit_pattern = re.compile("^([+-e\d\.]+)([kmgtp])$", re.IGNORECASE)

writer = csv.writer(sys.stdout)
for record in csv.reader(sys.stdin):
  for i, val in enumerate(record):
    m = unit_pattern.match(val) 
    if m:
      record[i] = conv(float(m.group(1)), m.group(2))
  writer.writerow(record)

