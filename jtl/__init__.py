#!/usr/bin/env python3

import json
import sys

def transform(data, transform):
	#TODO
	return data

	return None

def transformJson(data, transformData):
	result = {}
	for k, v in transformData.items():
		result[k] = transform(data, v)
	return result

def main():
	#TODO: parse arguments

	data = json.loads(sys.stdin.read())

	transformData = {} #TODO

	#Transform the JSON
	result = transformJson(data, transformData)

	#Output the result
	print(json.dumps(data, indent=4, sort_keys=True))

	return 0

if __name__ == '__main__':
	sys.exit(main())
