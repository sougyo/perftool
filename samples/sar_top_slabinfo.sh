#!/bin/bash

if [ $# -ne 3 ]; then
  echo "Usage: ${0##*/} sar top slabinfo"
  exit 1
fi

PATH=$(cd $(dirname $0)/..;pwd):$PATH

tmpdir=`mktemp -d /tmp/perf_workdir.XXXXXX`

if [ -z "$tmpdir" ]; then
  echo "Error: tmpdir"
  exit 1
fi

mkdir -p $tmpdir

function make_tmp_out() {
  out=`mktemp $tmpdir/${item}.XXXXXX`
  OUTFILES+=" $out"
}

OUTFILES=""
for item in sar-u sar-w sar-W sar-B sar-d sar-nDEV sar-mCPU sar-q sar-r sar-S ; do
  make_tmp_out
  x2csv.py -t $item $1 | csv2matrix.py > $out
done

make_tmp_out
x2csv.py -t top $2 | grep -E "%CPU|%MEM" | csv2matrix.py > $out

make_tmp_out
x2csv.py -t slabinfo $3 | grep active_objs | csv2matrix.py > $out

filter.py $OUTFILES

rm -f $OUTFILES
rmdir $tmpdir
