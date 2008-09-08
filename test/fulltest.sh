#!/bin/sh

if [ $@ ] ; then
    PYVERSIONS=$@
else
    PYVERSIONS="2.2 2.3 2.4"
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