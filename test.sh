#!/bin/bash

TESTS="faa1 test1"

for TEST in $TESTS
do
	echo "********** $TEST **********"

	INPUT=tests/$TEST.json
	OUTPUT=tests/$TEST.result

	diff $OUTPUT <(cat $INPUT | ./jtl/__init__.py -t tests/$TEST.jtl)
done
