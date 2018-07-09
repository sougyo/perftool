#!/usr/bin/env python

import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='performance info filter')
parser.add_argument('--regex'           , type=str, help='column filter regexp')
parser.add_argument('--start_index'     , type=int, help='start index')
parser.add_argument('--end_index'       , type=int, help='end index')
parser.add_argument('--avg_top_n'       , type=int, help='show only top n result by average')
parser.add_argument('--max_top_n'       , type=int, help='show only top n result by max')
parser.add_argument('--fillna'          , type=float, help='fill N/A with value')
parser.add_argument('--start_time'      , type=str, help='start time')
parser.add_argument('--end_time'        , type=str, help='end time')
parser.add_argument('-i', '--index_name', type=str, help='index name')
parser.add_argument('--column_prefix'   , type=str, help='column prefix')
parser.add_argument('--resample'        , type=str, help='resample (e.g. 5S)')
parser.add_argument('--csv_float_format', type=str, help='csv float format (e.g. %.1f)')
parser.add_argument('--max'             , action='store_true', help='max')
parser.add_argument('--min'             , action='store_true', help='min')
parser.add_argument('--mean'            , action='store_true', help='mean')
parser.add_argument('--median'          , action='store_true', help='median')
parser.add_argument('--sum'             , action='store_true', help='sum')
parser.add_argument('--transpose'       , action='store_true', help='transpose')
parser.add_argument('--normalize'       , action='store_true', help='normalize')
parser.add_argument('--standardize'     , action='store_true', help='standardize')
parser.add_argument('--columns'         , action='store_true', help='columns')
parser.add_argument('--describe'        , action='store_true', help='describe')
parser.add_argument('--label_with_index', action='store_true', help='label with index')
parser.add_argument('--dropna'          , action='store_true', help='drop N/A columns')
parser.add_argument('filepaths'         , nargs='*')
args = parser.parse_args()

csv_opt = { 'float_format': args.csv_float_format or '%.1f' }

filepaths = args.filepaths or [sys.stdin]

dfs = [pd.read_csv(f, index_col=(args.index_name or 'time')) for f in filepaths]
if args.regex:
  dfs = [df.filter(regex=args.regex) for df in dfs]

if args.end_index is not None:
  dfs = [df[:(args.end_index + 1)] for df in dfs]

if args.start_index is not None:
  dfs = [df[args.start_index:] for df in dfs]

if args.column_prefix:
  df.columns = map(lambda x: args.column_prefix + x, df.columns)

if args.label_with_index:
  for i, df in enumerate(dfs):
    df.columns = map(lambda x: str(i) + "_" + x,df.columns)

df = pd.concat(dfs, axis=1)
df.index.name = args.index_name or 'time'

cond = [True] * len(df.index)

def to_datetime(s):
  return pd.to_datetime(s, format='%H:%M:%S')

if args.start_time:
  cond &= (to_datetime(args.start_time) <= to_datetime(df.index))

if args.end_time:
  cond &= (to_datetime(args.end_time)   >= to_datetime(df.index))

df = df[cond]

if args.resample:
  df.index = pd.to_datetime(df.index, format='%H:%M:%S')
  df = df.resample(args.resample, label='right', closed='right').mean()
  df.index = df.index.strftime('%H:%M:%S')
  df.index.name = args.index_name or 'time'

if args.avg_top_n is not None:
  df = df[df.mean().sort_values(ascending=False)[:args.avg_top_n].index]
elif args.max_top_n is not None:
  df = df[df.max().sort_values(ascending=False)[:args.max_top_n].index]

if args.transpose:
  df = df.transpose()

if args.columns:
  for c in df.columns:
    print(c)
  sys.exit(0)

if args.describe:
  print(df.describe().to_csv(**csv_opt))
  sys.exit(0)

if args.normalize:
  df = df.apply(lambda x: (x - x.min()) / (x.max() - x.min()), axis=0)

if args.standardize:
  df = df.apply(lambda x: (x - x.mean())/x.std(), axis=0)

if args.fillna is not None:
  df = df.fillna(args.fillna)

if args.dropna:
  df = df.dropna(axis=1)

if args.max:
  print(df.max().to_frame().to_csv(**csv_opt))
elif args.min:
  print(df.min().to_frame().to_csv(**csv_opt))
elif args.mean:
  print(df.mean().to_frame().to_csv(**csv_opt))
elif args.median:
  print(df.median().to_frame().to_csv(**csv_opt))
elif args.sum:
  print(df.sum().to_frame().to_csv(**csv_opt))
else:
  print(df.to_csv(**csv_opt))
