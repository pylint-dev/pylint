#!/bin/sh

if [ $@ ] ; then
    PYVERSIONS=$@
else
    PYVERSIONS=`pyversions -iv`
fi

cd `dirname $0`

for ver in $PYVERSIONS; do  
    echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    echo `python$ver -V`
    echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    python$ver `which pytest`
    echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    echo `python$ver -V` -OO
    python$ver -OO `which pytest`
done
