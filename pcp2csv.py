#!/usr/bin/env python

import yaml
import subprocess
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='convert pcp archive into csv')
parser.add_argument('--config', type=str,
  default=os.path.join(os.path.dirname(__file__), "lib/pcp_config.yaml"))
parser.add_argument('--opts', type=str, default="")
parser.add_argument('archive', type=str)
parser.add_argument('outdir' , type=str)
args = parser.parse_args()

def exec_command(cmd):
  return subprocess.Popen(
    cmd,
    shell  = True,
    stdin  = subprocess.PIPE,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE).communicate()

config = {}
with open(args.config) as f:
  config = yaml.load(f)

if not os.path.exists(args.outdir):
  os.mkdir(args.outdir)

for data in config['data']:
  out = os.path.join(args.outdir, data['out'])
  print(out)

  metrics = " ".join(data['metrics'])
  for m in data['metrics']:
    print(" " + m)

  cmd = (
      '/usr/bin/python /usr/bin/pmrep -o csv -f "%H:%M:%S" -a {} {} {} '
      '| sed "1s/^Time/time/g" > {}'
    ).format(
      args.archive, args.opts, metrics, out
    )

  _, stderr = exec_command(cmd)

  if stderr:
    sys.stderr.write(stderr)

