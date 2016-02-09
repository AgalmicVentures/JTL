#!/usr/bin/env python3

import argparse
import base64
import json
import math
import sys

def maybe(f):
	return lambda x: f(x) if x is not None else None

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

	'abs': maybe(abs),

	#None
	'isNull': lambda x: x is None,

	'default': lambda x, y: x if x is not None else y,
	'defaultNan': lambda x: x if x is not None else float('nan'),

	#Bool
	'not': maybe(lambda x: not x),

	#Dict
	'keys': maybe(lambda d: d.keys()),
	'values': maybe(lambda d: d.values()),

	#Float
	'isFinite': maybe(lambda x: math.isfinite(x)),
	'isNan': maybe(lambda x: math.isnan(x)),

	'ceil': maybe(lambda x: math.ceil(x)),
	'cos': maybe(lambda x: math.cos(x)),
	'cosh': maybe(lambda x: math.cosh(x)),
	'erf': maybe(lambda x: math.erf(x)),
	'exp': maybe(lambda x: math.exp(x)),
	'floor': maybe(lambda x: math.floor(x)),
	'lg': maybe(lambda x: math.log2(x)),
	'ln': maybe(lambda x: math.log(x)),
	'log': maybe(lambda x: math.log10(x)),
	'sin': maybe(lambda x: math.sin(x)),
	'sinh': maybe(lambda x: math.sinh(x)),
	'sqrt': maybe(lambda x: math.sqrt(x)),
	'tan': maybe(lambda x: math.tan(x)),
	'tanh': maybe(lambda x: math.tanh(x)),

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
	'length': maybe(len),

	'first': lambda s: s[0] if s is not None and len(s) > 1 else None,
	'rest': lambda s: s[1:] if s is not None and len(s) > 1 else None,
	'last': lambda s: s[-1] if s is not None and len(s) > 1 else None,
	'init': lambda s: s[:-1] if s is not None and len(s) > 1 else None,

	'sorted': maybe(lambda s: list(sorted(s))),
	'unique': maybe(lambda s: list(set(s))),

	'sum': maybe(sum),
	#TODO: average
	#TODO: stddev
	#TODO: statistics

	'min': maybe(min),
	'max': maybe(max),

	'count': lambda s, f: s.count(f) if s is not None and f is not None else None,

	#String
	'lower': maybe(lambda s: s.lower()),
	'upper': maybe(lambda s: s.upper()),
	'capitalize': maybe(lambda s: s.capitalize()),

	'find': lambda s, f: s.find(f) if s is not None and f is not None else None,
	'strip': maybe(lambda s: s.strip()),
	'startsWith': lambda s, f: s.startswith(f) if s is not None and f is not None else None,
	'endsWith': lambda s, f: s.endswith(f) if s is not None and f is not None else None,

	'join': lambda s, *args: (args[0] if len(args) > 0 else '').join(s) if s is not None else None,
	'split': lambda s, sp: s.split(sp) if s is not None and sp is not None  else None,
	'lines': maybe(lambda s: s.split('\n')),
	'unlines': maybe(lambda s: '\n'.join(s)),
	'words': maybe(lambda s: s.split(' ')),
	'unwords': maybe(lambda s: ' '.join(s)),
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

		#Nothing found -- error!
		raise NameError(operation)

	return function(value, *args)

def parseArgument(argument, data):
	try:
		#Try loading as a constrant first
		#TODO: strings are awkward and require escaping, so figure that out
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
	#Parse arguments
	parser = argparse.ArgumentParser(description='JSON Transformation Language')
	parser.add_argument('-i', '--indent', default=4, type=int, help='Indentation amount.')
	parser.add_argument('transform', help='The transformation to run.')

	arguments = parser.parse_args(sys.argv[1:])
	transformData = json.loads(arguments.transform)

	#Read the JSON in from stdin
	#TODO: error handling
	data = json.loads(sys.stdin.read())

	#Transform the JSON
	result = transformJson(data, transformData)

	#Output the result
	print(json.dumps(result, indent=arguments.indent, sort_keys=True))

	return 0

if __name__ == '__main__':
	sys.exit(main())
