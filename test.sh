#!/bin/bash

TESTS=faa1

for TEST in $TESTS
do
	echo "********** $TEST **********"

	INPUT=tests/$TEST.jsonw
	TRANSFORM=`cat tests/$TEST.jtl`
	OUTPUT=tests/$TEST.jtl

	cat $INPUT | ./jtl/__init__.py "$TRANSFORM"
done
