#!/usr/bin/env python3

import argparse
import json
import sys

import Interpreter

def main():
	"""
	Runs the main JTL program.

	:return: int
	"""

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
	result = Interpreter.transformJson(data, transformData)

	#Output the result
	print(json.dumps(result, indent=arguments.indent, sort_keys=True))

	return 0

if __name__ == '__main__':
	sys.exit(main())
