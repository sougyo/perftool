#!/usr/bin/env python

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse

parser = argparse.ArgumentParser(description='performance info converter')
parser.add_argument('-w'          , default=None, type=str, help='output file')
parser.add_argument('--regex'     , default=None, type=str, help='column filter regexp')
parser.add_argument('--ylim_min'  , default=None, type=int, help='ylim min')
parser.add_argument('--ylim_max'  , default=None, type=int, help='ylim max')
parser.add_argument('--ylabel'    , default=None, type=str, help='ylabel')
parser.add_argument('--title'     , default=None, type=str, help='graph title')
parser.add_argument('--stack'     , action='store_true', help='stacked graph')
parser.add_argument('--width'     , default=11,   type=int, help='width')
parser.add_argument('--height'    , default=6,    type=int, help='height')
parser.add_argument('--yformatter', default="{x:,.0f}", type=str, help='y axis formatter')
parser.add_argument('--rot'       , default=0, type=str, help='rot')
args = parser.parse_args()

df = pd.read_csv(sys.stdin, index_col='time')
if args.regex:
  df = df.filter(regex=args.regex)

plot_option = {}
plot_option["rot"] = args.rot
plot_option["figsize"] = (args.width, args.height)
if args.stack:
  plot_option['kind'] = 'area'
  plot_option['stacked'] = True
  plot_option['linewidth'] = 0

ax = df.plot(**plot_option)
ax.set_xticklabels(df.index)
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(args.yformatter))

if args.ylabel:
  plt.ylabel(args.ylabel)

if args.title:
  plt.title(args.title)

ymin, ymax = plt.ylim()
if args.ylim_min != None:
  ymin = args.ylim_min
if args.ylim_max != None:
  ymax = args.ylim_max
plt.ylim(ymin, ymax)

if args.w:
#  ax.get_figure().savefig(args.w)
  plt.savefig(args.w)
else:
  plt.show()


