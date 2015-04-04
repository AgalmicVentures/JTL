#!/usr/bin/env python3

import json
import math
import sys

functions = {
	#Any
	'toString': lambda x: str(x),

	#None
	'isNull': lambda x: x is None,

	'defaultEmpty': lambda x: x if x is not None else '',
	'defaultNan': lambda x: x if x is not None else float('nan'),
	'defaultZero': lambda x: x if x is not None else 0,

	#Bool
	'not': lambda x: not x if x is not None else None,

	#Dict
	'keys': lambda d: d.keys() if d is not None else None,
	'values': lambda d: d.values() if d is not None else None,

	#Float
	'isNan': lambda x: math.isnan(x) if x is not None else None,

	#Int
	'isZero': lambda x: x == 0 if x is not None else None,

	#Sequence
	'length': lambda s: len(s) if s is not None else 0,

	'first': lambda s: s[0] if s is not None and len(s) > 1 else None,
	'rest': lambda s: s[1:] if s is not None and len(s) > 1 else None,
	'last': lambda s: s[-1] if s is not None and len(s) > 1 else None,
	'init': lambda s: s[:-1] if s is not None and len(s) > 1 else None,

	'sum': lambda s: sum(s) if s is not None else 0,

	#String
	'lower': lambda s: s.lower() if s is not None else 0,
	'upper': lambda s: s.upper() if s is not None else 0,
	'capitalize': lambda s: s.capitalize() if s is not None else 0,

	'strip': lambda s: s.strip() if s is not None else 0,

	'join': lambda s: ''.join(s) if s is not None else None,
	'lines': lambda s: s.split('\n') if s is not None else None,
	'unlines': lambda s: '\n'.join(s) if s is not None else None,
	'words': lambda s: s.split(' ') if s is not None else None,
	'unwords': lambda s: ' '.join(s) if s is not None else None,
}

def parseTransform(transform):
	#TODO: multi-level selectors
	#TODO: more robust parsing
	#TODO: handle arguments
	return [token.strip() for token in transform.split('$')]

def applyOperation(value, operation):
	function = functions.get(operation)
	if function is None:
		#TODO: error
		return None

	return function(value)

def transform(data, transform):
	#Parse the transformation into tokens
	tokens = parseTransform(transform)
	if len(tokens) == 0:
		return None

	primarySelector = tokens[0]
	value = data.get(primarySelector)
	for operation in tokens[1:]:
		value = applyOperation(value, operation)

	return value #TODO: transform it too

def transformJson(data, transformData):
	result = {}
	for k, v in transformData.items():
		result[k] = transform(data, v)
	return result

def main():
	#TODO: parse arguments properly
	transformStr = sys.argv[1]
	transformData = json.loads(transformStr)

	#Read the JSON in from stdin
	#TODO: error handling
	data = json.loads(sys.stdin.read())

	#Transform the JSON
	result = transformJson(data, transformData)

	#Output the result
	print(json.dumps(result, indent=4, sort_keys=True))

	return 0

if __name__ == '__main__':
	sys.exit(main())
