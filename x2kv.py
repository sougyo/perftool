#!/usr/bin/env python

import argparse
import json
import csv
import re
import os
import sys
import lib.table

parser = argparse.ArgumentParser(description='performance info converter')
parser.add_argument('-t', default=None, help=
  "specify a type of perftool, such as 'sar-w' (see lib/spec.json)")
parser.add_argument('--hint_file', type=str,
  default=os.path.join(os.path.dirname(__file__), "lib/hint.json"))
parser.add_argument('--spec_file', type=str,
  default=os.path.join(os.path.dirname(__file__), "lib/spec.json"))
parser.add_argument('--strict', action='store_true', help='strict type')
parser.add_argument('filepath', nargs='?')
args = parser.parse_args()

with open(args.spec_file) as f:
  spec_dict = json.load(f)

with open(args.hint_file) as f:
  hint_dict  = json.load(f)

key_list = []
if args.strict and args.t:
  key_list.append(args.t)
else:
  if args.t:
    key_list.extend(filter(lambda k: re.search(args.t, k), spec_dict))

  basename = os.path.basename(args.filepath) if args.filepath else 'sar'
  for l in map(lambda h: h["list"],
             filter(lambda x: re.search(x["pattern"], basename), hint_dict)):
    key_list.extend(l)

from io import open
f = open(args.filepath, 'r', encoding='utf-8') if args.filepath else sys.stdin
writer = csv.writer(sys.stdout)
out = False
try:
  for k in key_list:
    if args.filepath:
      f.seek(0)
    for a in lib.table.Table(f, **spec_dict[k]):
      writer.writerow(a)
      sys.stdout.flush()
      out = True
    if out:
      break
finally:
  f.close()
