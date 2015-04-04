#!/usr/bin/env python3

import json
import sys

def parseTransform(transform):
	return [token.strip() for token in transform.split('$')]

def transform(data, transform):
	#Parse the transformation into tokens
	tokens = parseTransform(transform)
	if len(tokens) == 0:
		return None

	primarySelector = tokens[0]
	value = data.get(primarySelector)

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
