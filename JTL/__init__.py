#!/usr/bin/env python3

import base64
import json
import math
import sys

def extractPath(data, path):
	splitPath = path.split('.')
	return extractSplitPath(data, splitPath)

def extractSplitPath(data, splitPath):
	nextData = data.get(splitPath[0])
	return nextData if len(splitPath) <= 1 or nextData is None else extractSplitPath(nextData, splitPath[1:])

def toBool(data):
	return data == 'True' or data == 'true'

def toFloat(data):
	try:
		return float(data)
	except ValueError:
		return None

def toInt(data):
	try:
		return int(data)
	except ValueError:
		return None

def toNumber(data):
	intValue = toInt(data)
	if intValue is not None:
		return intValue

	return toFloat(data)

functions = {
	#Any
	'toString': str,
	'toBool': toBool,
	'toFloat': toFloat,
	'toInt': toInt,
	'toNumber': toNumber,

	'abs': lambda x: abs(x) if x is not None else None,

	#None
	'isNull': lambda x: x is None,

	'default': lambda x, y: x if x is not None else y, #TODO: parsing, rather than just always doing a string
	'defaultNan': lambda x: x if x is not None else float('nan'),

	#Bool
	'not': lambda x: not x if x is not None else None,

	#Dict
	'keys': lambda d: d.keys() if d is not None else None,
	'values': lambda d: d.values() if d is not None else None,

	#Float
	'isFinite': lambda x: math.isfinite(x) if x is not None else None,
	'isNan': lambda x: math.isnan(x) if x is not None else None,

	'ceil': lambda x: math.ceil(x) if x is not None else None,
	'cos': lambda x: math.cos(x) if x is not None else None,
	'cosh': lambda x: math.cosh(x) if x is not None else None,
	'erf': lambda x: math.erf(x) if x is not None else None,
	'exp': lambda x: math.exp(x) if x is not None else None,
	'floor': lambda x: math.floor(x) if x is not None else None,
	'lg': lambda x: math.log2(x) if x is not None else None,
	'ln': lambda x: math.log(x) if x is not None else None,
	'log': lambda x: math.log10(x) if x is not None else None,
	'sin': lambda x: math.sin(x) if x is not None else None,
	'sinh': lambda x: math.sinh(x) if x is not None else None,
	'sqrt': lambda x: math.sqrt(x) if x is not None else None,
	'tan': lambda x: math.tan(x) if x is not None else None,
	'tanh': lambda x: math.tanh(x) if x is not None else None,

	#Int

	#Numer
	'+': lambda x, y: x + y if x is not None and y is not None else None,
	'-': lambda x, y: x - y if x is not None and y is not None else None,
	'*': lambda x, y: x * y if x is not None and y is not None else None,
	'/': lambda x, y: x / y if x is not None and y is not None else None,
	'**': lambda x, y: x ** y if x is not None and y is not None else None,
	'%': lambda x, y: x % y if x is not None and y is not None else None,

	'==': lambda x, y: x == y if x is not None and y is not None else None,
	'!=': lambda x, y: x != y if x is not None and y is not None else None,
	'<': lambda x, y: x < y if x is not None and y is not None else None,
	'<=': lambda x, y: x <= y if x is not None and y is not None else None,
	'>': lambda x, y: x > y if x is not None and y is not None else None,
	'>=': lambda x, y: x >= y if x is not None and y is not None else None,

	#Sequence
	'length': lambda s: len(s) if s is not None else None,

	'first': lambda s: s[0] if s is not None and len(s) > 1 else None,
	'rest': lambda s: s[1:] if s is not None and len(s) > 1 else None,
	'last': lambda s: s[-1] if s is not None and len(s) > 1 else None,
	'init': lambda s: s[:-1] if s is not None and len(s) > 1 else None,

	'sorted': lambda s: list(sorted(s)) if s is not None else None,
	'unique': lambda s: list(set(s)) if s is not None else None,

	'sum': lambda s: sum(s) if s is not None else None,
	#TODO: average
	#TODO: stddev
	#TODO: statistics

	'min': lambda s: min(s) if s is not None else None,
	'max': lambda s: max(s) if s is not None else None,

	'count': lambda s, f: s.count(f) if s is not None and f is not None else None,

	#String
	'lower': lambda s: s.lower() if s is not None else None,
	'upper': lambda s: s.upper() if s is not None else None,
	'capitalize': lambda s: s.capitalize() if s is not None else None,

	'find': lambda s, f: s.find(f) if s is not None and f is not None else None,
	'strip': lambda s: s.strip() if s is not None else None,
	'startsWith': lambda s, f: s.startswith(f) if s is not None and f is not None else None,
	'endsWith': lambda s, f: s.endswith(f) if s is not None and f is not None else None,

	'join': lambda s, *args: (args[0] if len(args) > 0 else '').join(s) if s is not None else None,
	'split': lambda s, sp: s.split(sp) if s is not None and sp is not None  else None,
	'lines': lambda s: s.split('\n') if s is not None else None,
	'unlines': lambda s: '\n'.join(s) if s is not None else None,
	'words': lambda s: s.split(' ') if s is not None else None,
	'unwords': lambda s: ' '.join(s) if s is not None else None,
}

def parseTransform(transform):
	#TODO: more robust parsing
	#TODO: handle arguments
	return [
		[token for token in tokens.split(' ') if token != '']
		for tokens in transform.split('$')
	]

def applyOperation(value, operation, args):
	function = functions.get(operation)
	if function is None:
		#Is it a simple integer index?
		index = toInt(operation)
		if index is not None:
			return value[index]

		#Or perhaps it's a selector function? .abc.def
		if len(args) == 0 and operation[0] == '.':
			return extractPath(value, operation[1:])

		#TODO: error
		return None

	return function(value, *args)

def parseArgument(argument, data):
	try:
		#Try loading as a constrant first
		return json.loads(argument)
	except ValueError:
		#If that fails, it might be a name
		return extractPath(data, argument)

def transform(data, transform):
	#Parse the transformation into tokens
	tokens = parseTransform(transform)
	if len(tokens) == 0:
		return None

	primarySelector = tokens[0][0]
	value = extractPath(data, primarySelector)
	for section in tokens[1:]:
		operation = section[0]
		args = [parseArgument(argument, data) for argument in section[1:]]
		value = applyOperation(value, operation, args)

	return value #TODO: transform it too

def transformJson(data, transformData):
	if type(transformData) is dict:
		result = {}
		for k, v in transformData.items():
			result[k] = transformJson(data, v)
	elif type(transformData) is str:
		result = transform(data, transformData)
	else:
		result = None
	return result

def main():
	if len(sys.argv) < 2:
		print('Usage: jtl <TRANSFORM>')
		return 0 #TODO: different code

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
