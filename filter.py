#!/usr/bin/env python

import sys
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='performance info filter')
parser.add_argument('--regex'           , type=str, help='column filter regexp')
parser.add_argument('--start_index'     , type=int, help='start index')
parser.add_argument('--end_index'       , type=int, help='end index')
parser.add_argument('--left_n'          , type=int, help='show only left n columns')
parser.add_argument('--fillna'          , type=float, help='fill N/A with value')
parser.add_argument('--start_time'      , type=str, help='start time')
parser.add_argument('--end_time'        , type=str, help='end time')
parser.add_argument('-i', '--index_name', type=str, help='index name')
parser.add_argument('--column_prefix'   , type=str, help='column prefix')
parser.add_argument('--resample'        , type=str, help='resample (e.g. 5S)')
parser.add_argument('--csv_float_format', type=str, help='csv float format (e.g. %.1f)')
parser.add_argument('--max'             , action='store_true', help='max')
parser.add_argument('--min'             , action='store_true', help='min')
parser.add_argument('--avg'             , action='store_true', help='average')
parser.add_argument('--median'          , action='store_true', help='median')
parser.add_argument('--sum'             , action='store_true', help='sum')
parser.add_argument('--std'             , action='store_true', help='std')
parser.add_argument('--transpose'       , action='store_true', help='transpose')
parser.add_argument('--normalize'       , action='store_true', help='normalize')
parser.add_argument('--standardize'     , action='store_true', help='standardize')
parser.add_argument('--columns'         , action='store_true', help='columns')
parser.add_argument('--describe'        , action='store_true', help='describe')
parser.add_argument('--label_with_index', action='store_true', help='label with index')
parser.add_argument('--dropna'          , action='store_true', help='drop N/A columns')
parser.add_argument('--sort_by_avg'     , action='store_true', help='sort columns by avg')
parser.add_argument('--sort_by_max'     , action='store_true', help='sort columns by max')
parser.add_argument('--sort_by_std'     , action='store_true', help='sort columns by std')
parser.add_argument('filepaths'         , nargs='*', help='prefix_tag:filepath:postfix_tag ...')
args = parser.parse_args()

csv_opt = { 'float_format': args.csv_float_format or '%.1f' }

filepaths = args.filepaths or [sys.stdin]

def make_df(tagged_path, index_col):
  prefix_tag = ""
  postfix_tag = ""

  c = tagged_path.count(":") if isinstance(tagged_path, str) else 0
  if c > 1:
    prefix_tag, path, postfix_tag = tagged_path.split(":", 2)
  elif c == 1:
    prefix_tag, path = tagged_path.split(":", 1)
  else:
    path = tagged_path

  df = pd.read_csv(path, index_col=index_col)
  if prefix_tag or postfix_tag:
    df.columns = [prefix_tag + column + postfix_tag for column in df.columns]

  return df

dfs = [make_df(f, args.index_name or 'time') for f in filepaths]
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

if args.fillna is not None:
  df = df.fillna(args.fillna)

if args.dropna:
  df = df.dropna(axis=1)

if args.resample:
  df.index = pd.to_datetime(df.index, format='%H:%M:%S')
  df = df.resample(args.resample, label='right', closed='right').mean()
  df.index = df.index.strftime('%H:%M:%S')
  df.index.name = args.index_name or 'time'

if args.sort_by_avg:
  df = df[df.mean().sort_values(ascending=False).index]
elif args.sort_by_max:
  df = df[df.max().sort_values(ascending=False).index]
elif args.sort_by_std:
  df = df[df.std().sort_values(ascending=False).index]

if args.left_n is not None:
  df = df.iloc[:,:args.left_n]

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


stats = { "series": [], "keys": [] }

def append_stat(key, series):
  stats["series"].append(series)
  stats["keys"].append(key)

if args.min:
  append_stat("min", df.min())
if args.avg:
  append_stat("avg", df.mean())
if args.median:
  append_stat("median", df.median())
if args.max:
  append_stat("max", df.max())
if args.sum:
  append_stat("sum", df.sum())
if args.std:
  append_stat("std", df.std())

if stats["series"]:
  print(pd.concat(stats["series"], keys=stats["keys"], axis=1).to_csv(**csv_opt))
else:
  print(df.to_csv(**csv_opt))

