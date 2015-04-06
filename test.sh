#!/bin/bash

TESTS=faa1

for TEST in $TESTS
do
	echo "********** $TEST **********"

	INPUT=tests/$TEST.json
	TRANSFORM=`cat tests/$TEST.jtl`
	OUTPUT=tests/$TEST.result

	diff $OUTPUT <(cat $INPUT | ./jtl/__init__.py "$TRANSFORM")
done
