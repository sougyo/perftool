#!/usr/bin/env python

import sys
import csv
import re
import lib.table

if len(sys.argv) != 2:
  sys.stderr.write("Usage: x2csv.py filename\n")
  sys.exit(1)

path = sys.argv[1]

writer = csv.writer(sys.stdout)
with open(path) as f:
  t = []
  if re.search(r"\bsar", path):
    t = lib.table.Table(f, "idle", subkey_column="CPU")
  if re.search(r"mpstat", path):
    t = lib.table.Table(f, "idle", subkey_column="CPU")
  if re.search(r"iostat", path):
    t = lib.table.Table(f, "rrqm", subkey_column="Device:", time_regexp=r"\d\d/\d\d/\d\d (\d\d:\d\d:\d\d)")
  if re.search(r"\bps", path):
    t = lib.table.Table(f, "PID", exact=False, subkey_column="PID", time_regexp=r"^Time:\s+(\d\d:\d\d:\d\d)")
  if re.search(r"\btop", path):
    t = lib.table.Table(f, "COMMAND", exact=False, subkey_column="PID", time_regexp=r"top \- (\d\d:\d\d:\d\d)")
  if re.search(r"interrupts", path):
    t = lib.table.Table(f, "CPU", exact=False, subkey_column="HEAD", time_regexp=r"^Time:\s+(\d\d:\d\d:\d\d)",
                                  column_head="HEAD", column_tail="TAIL")
  if re.search(r"numastat", path):
    t = lib.table.Table(f, "node0", subkey_column="HEAD", time_regexp=r"^Time:\s+(\d\d:\d\d:\d\d)", column_head="HEAD")
#  if re.search("slabinfo", path):
#    t = lib.table.Table(f, "name", subkey_column="name", exact=False, time_regexp="^Time:\s+(\d\d:\d\d:\d\d)",
                                   
  for a in t:
    writer.writerow(a)
 
