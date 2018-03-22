#!/usr/bin/env python

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse

parser = argparse.ArgumentParser(description='performance info converter')
parser.add_argument('-w'           , default=None, type=str, help='output image file')
parser.add_argument('--regex'      , default=None, type=str, help='column filter regexp')
parser.add_argument('--ylim_min'   , default=None, type=int, help='ylim min')
parser.add_argument('--ylim_max'   , default=None, type=int, help='ylim max')
parser.add_argument('--ylabel'     , default=None, type=str, help='ylabel')
parser.add_argument('--title'      , default=None, type=str, help='graph title')
parser.add_argument('--stack'      , action='store_true', help='stacked graph')
parser.add_argument('--width'      , default=11,   type=int, help='width')
parser.add_argument('--height'     , default=6,    type=int, help='height')
parser.add_argument('--yformatter' , default="{x:,.0f}", type=str, help='y axis formatter')
parser.add_argument('--rot'        , default=0, type=str, help='rot')
parser.add_argument('--legend_loc' , default=None, type=str, help='legend location "(upper|lower|center) (left|right|center)"')
parser.add_argument('--legend_uniq', action='store_true', help='show legend only on the bottom of graph')
parser.add_argument('filepaths'    , nargs='*')
args = parser.parse_args()

filepaths = args.filepaths or [sys.stdin]

dfs = [pd.read_csv(f, index_col='time') for f in filepaths]
dfs = [(df.filter(regex=args.regex) if args.regex else df) for df in dfs]

fig, ax_list = plt.subplots(nrows=len(dfs))
if len(dfs) == 1:
  ax_list = [ax_list]

ylims = []
for df, ax in zip(dfs, ax_list):
  plot_option = {}
  plot_option["rot"] = args.rot
  plot_option["figsize"] = (args.width, args.height)
  plot_option["ax"] = ax
  if args.stack:
    plot_option['kind'] = 'area'
    plot_option['stacked'] = True
    plot_option['linewidth'] = 0
  ax.set_xticklabels(df.index)
  ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(args.yformatter))
  df.plot(**plot_option)

  ylims.append(ax.get_ylim())

y_min = min([y[0] for y in ylims])
y_max = max([y[1] for y in ylims])
if args.ylim_min != None:
  y_min = args.ylim_min
if args.ylim_max != None:
  y_max = args.ylim_max

for i, ax in enumerate(ax_list):
  ax.set_ylim(y_min, y_max)

  if args.legend_uniq and (i != 0):
    ax.legend([""])
  elif args.legend_loc:
    ax.legend(loc=args.legend_loc)


if args.ylabel:
  plt.ylabel(args.ylabel)

if args.title:
  plt.title(args.title)

if args.w:
  plt.savefig(args.w)
else:
  plt.show()

