#!/usr/bin/env python

import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='performance info filter')
parser.add_argument('--regex'       , default=None, type=str, help='column filter regexp')
parser.add_argument('--start_index' , default=None, type=int, help='start index')
parser.add_argument('--end_index'   , default=None, type=int, help='end index')
parser.add_argument('--max'         , action='store_true', help='max')
parser.add_argument('--min'         , action='store_true', help='min')
parser.add_argument('--mean'        , action='store_true', help='mean')
parser.add_argument('--sum'         , action='store_true', help='sum')
parser.add_argument('--transpose'   , action='store_true', help='transpose')
parser.add_argument('--normalize'   , action='store_true', help='normalize')
parser.add_argument('filepaths'     , nargs='*')
args = parser.parse_args()

filepaths = args.filepaths or [sys.stdin]

dfs = [pd.read_csv(f, index_col='time') for f in filepaths]
if args.regex:
  dfs = [df.filter(regex=args.regex) for df in dfs]

if args.end_index:
  dfs = [df[:(args.end_index + 1)] for df in dfs]

if args.start_index:
  dfs = [df[args.start_index:] for df in dfs]

df = pd.concat(dfs, axis=1)

def f(s):
  d = s.max() - s.min()
  if d == 0:
    if s.max() == 0:
      return s
    elif d == 0:
      return s / s.max()
  else:
    return (s - s.min())/d

if args.normalize:
  df = df.apply(f, axis=0)

if args.transpose:
  df = df.transpose()

if args.max:
  print(df.max().to_frame().to_csv())
elif args.min:
  print(df.min().to_frame().to_csv())
elif args.mean:
  print(df.mean().to_frame().to_csv())
elif args.sum:
  print(df.sum().to_frame().to_csv())
else:
  print(df.to_csv())
