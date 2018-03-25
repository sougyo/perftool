#!/usr/bin/env python

import sys
import csv
import re
import lib.table
import argparse
import yaml
import os

table_yaml = yaml.load(open(os.path.join(os.path.dirname(__file__), "table.yaml"), "r+"))
hint_yaml  = yaml.load(open(os.path.join(os.path.dirname(__file__), "hint.yaml") , "r+"))

names = ', '.join([k for k in table_yaml])

parser = argparse.ArgumentParser(description='performance info converter')
parser.add_argument('-t', default=None, help=("specify a type of perftool: " + names))
parser.add_argument('filepath', nargs='?')
args = parser.parse_args()

key_list = []
if args.t:
  key_list.extend(filter(lambda k: re.search(args.t, k), table_yaml))

basename = os.path.basename(args.filepath) if args.filepath else 'sar'
for l in map(lambda h: h["list"], filter(lambda x: re.search(x["pattern"], basename), hint_yaml)):
  key_list.extend(l)

f = open(args.filepath) if args.filepath else sys.stdin
writer = csv.writer(sys.stdout)
out = False
try:
  for k in key_list:
    if args.filepath:
      f.seek(0)
    for a in lib.table.Table(f, **table_yaml[k]):
      writer.writerow(a)
      sys.stdout.flush()
      out = True
    if out:
      break
finally:
  f.close()
