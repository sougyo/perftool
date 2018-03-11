#!/usr/bin/env python

import sys
import csv
import re
import lib.table
import argparse
import yaml

parser = argparse.ArgumentParser(description='performance info converter')
parser.add_argument('-t', default="sar")
parser.add_argument('filepath')
args = parser.parse_args()

table_yaml = yaml.load(open("table.yaml", "r+"))

for h in list(filter(lambda x: re.search(args.t, x["name"]), table_yaml)):
  writer = csv.writer(sys.stdout)
  with open(args.filepath) as f:
    t = lib.table.Table(f, **h)

    for a in t:
      writer.writerow(a)
 
