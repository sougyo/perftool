#!/bin/bash

PATH=$(cd $(dirname $0)/..;pwd):$PATH

mkdir -p /tmp/perf_workdir

OUTFILES=""
for item in sar-u sar-w sar-W sar-B sar-d sar-nDEV sar-mCPU sar-q sar-r sar-S ; do
  out=`mktemp /tmp/perf_workdir/${item}.XXXXXX`
  OUTFILES+=" $out"
  x2csv.py -t $item $1 | csv2matrix.py > $out
done
filter.py $OUTFILES

rm -f $OUTFILES
rmdir /tmp/perf_workdir
