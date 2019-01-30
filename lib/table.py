#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import re

class Table:
  def __init__(self, fd, **options):
    self.fd            = fd
    self.column_regexp = re.compile(options["column_pattern"])
    tr                 = options.get("time_regexp")
    self.time_regexp   = tr and re.compile(tr)
    self.subkey_column = options.get("subkey_column")
    self.column_head   = options.get("column_head")
    self.column_tail   = options.get("column_tail")
    self.exact         = options.get("exact", True)
    self.columns       = None
    self.time_list     = collections.OrderedDict()
    self.gen           = self.generator()
    self.head_time_regexp = re.compile(r"^(\d\d)(:|時)(\d\d)(:|分)(\d\d)(秒)?\s+(.*)$")
    self.replace_old = options.get("replace_old")
    self.replace_new  = options.get("replace_new")

  def __iter__(self):
    return self

  def __next__(self):
    return self.gen.__next__()

  def next(self):
    return self.gen.next()

  def generator(self):
    cnt         = 0
    time        = None
    columns_len = None
    enabled     = False 
    while True:
      line = self.fd.readline()

      if not line:
        return

      line = line.strip()

      if self.replace_old and self.replace_new:
        line = line.replace(self.replace_old, self.replace_new)

      if self.time_regexp:
        m = self.time_regexp.search(line)
        if m:
          if m.lastindex == 1:
            time = m.group(1)
          else:
            cnt += 1
            time = cnt

      m = self.head_time_regexp.search(line)
      if m:
        time = "{}:{}:{}".format(m.group(1), m.group(3), m.group(5))
        line = m.group(7)

      if self.column_regexp.search(line):
        record = re.split("\s+", line)
        if self.column_head:
          record.insert(0, self.column_head)
        if self.column_tail:
          record.append(self.column_tail)
        if not self.columns:
          self.columns = record
          columns_len  = len(record)
        if record == self.columns:
          enabled = True
        continue

      if enabled:
        if time:
          self.time_list[time] = True
        record = re.split(r"\s+", line) if self.exact else re.split(r"\s+", line, columns_len - 1)

        if len(record) == columns_len:
          cr = list(zip(self.columns, record))
          s  = dict(cr).get(self.subkey_column)
          for (c, v) in cr:
            if c != self.subkey_column:
              yield([time, c, s, v])
        else:
          enabled = False


