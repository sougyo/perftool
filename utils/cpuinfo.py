#!/usr/bin/env python

import re
import sys

table = []
record = None
for line in sys.stdin:
  m = re.match("^processor\s*:\s*(\d+)$", line)
  if m:
    record = {}
    table.append(record)
    record["processor"] = m.groups()[0]

  m = re.match("^physical id\s*:\s*(\d+)$", line)
  if m:
    record["physical_id"] = m.groups()[0]

  m = re.match("^core id\s*:\s*(\d+)$", line)
  if m:
    record["core_id"] = m.groups()[0]

  m = re.match("^model name\s*:\s*(.*)$", line)
  if m:
    record["model_name"] = m.groups()[0]

for r in table:
  print("{},{},{},{}".format(
           r["physical_id"],
           r["core_id"],
           r["processor"],
           r["model_name"]))
