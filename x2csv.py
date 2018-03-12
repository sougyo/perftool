#!/usr/bin/env python

import sys
import csv
import re
import lib.table
import argparse
import yaml
import os

table_yaml = yaml.load(open("table.yaml", "r+"))
hint_yaml  = yaml.load(open("hint.yaml" , "r+"))

names = ', '.join([k for k in table_yaml])

parser = argparse.ArgumentParser(description='performance info converter')
parser.add_argument('-t', default=None, help=("specify a type of perftool: " + names))
parser.add_argument('filepath')
args = parser.parse_args()

key_list = []
if args.t:
  key_list.extend(filter(lambda k: re.search(args.t, k), table_yaml))

basename = os.path.basename(args.filepath)
for l in map(lambda h: h["list"], filter(lambda x: re.search(x["pattern"], basename), hint_yaml)):
  key_list.extend(l)

writer = csv.writer(sys.stdout)
out = False
for k in key_list:
  with open(args.filepath) as f:
    for a in lib.table.Table(f, **table_yaml[k]):
      writer.writerow(a)
      out = True
  if out:
    break

