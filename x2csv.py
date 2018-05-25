#!/usr/bin/env python

import sys
import csv
import re
import lib.table
import lib.table_dict
import lib.hint_dict
import argparse
import os

table_dict = lib.table_dict.get()
hint_dict  = lib.hint_dict.get()

names = ', '.join([k for k in table_dict])

parser = argparse.ArgumentParser(description='performance info converter')
parser.add_argument('-t', default=None, help=("specify a type of perftool: " + names))
parser.add_argument('filepath', nargs='?')
args = parser.parse_args()

key_list = []
if args.t:
  key_list.extend(filter(lambda k: re.search(args.t, k), table_dict))

basename = os.path.basename(args.filepath) if args.filepath else 'sar'
for l in map(lambda h: h["list"], filter(lambda x: re.search(x["pattern"], basename), hint_dict)):
  key_list.extend(l)

f = open(args.filepath) if args.filepath else sys.stdin
writer = csv.writer(sys.stdout)
out = False
try:
  for k in key_list:
    if args.filepath:
      f.seek(0)
    for a in lib.table.Table(f, **table_dict[k]):
      writer.writerow(a)
      sys.stdout.flush()
      out = True
    if out:
      break
finally:
  f.close()
