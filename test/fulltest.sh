#!/bin/sh

if [ $@ ] ; then
    PYVERSIONS=$@
else
    PYVERSIONS=`pyversions -iv`
fi

for ver in $PYVERSIONS; do  
    echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    echo `python$ver -V`
    echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    python$ver runtests.py
    echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    echo `python$ver -V` -OO
    python$ver -OO runtests.py
done
