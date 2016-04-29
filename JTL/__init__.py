#!/usr/bin/env python3

import argparse
import json
import sys

def main():
	"""
	Runs the main JTL program.

	:return: int
	"""

	#Parse arguments
	parser = argparse.ArgumentParser(description='JSON Transformation Language')
	parser.add_argument('-i', '--indent', default=4, type=int, help='Indentation amount.')
	parser.add_argument('-t', '--transform-file', help='The name of the JSON file containing the transformation to run.')
	parser.add_argument('transform', nargs='?', help='The transformation to run.')
	arguments = parser.parse_args(sys.argv[1:])

	#Load the transformation
	if arguments.transform is None and arguments.transform_file is not None:
		#From a file
		with open(arguments.transform_file, 'r') as f:
			transformStr = f.read()
	elif arguments.transform is not None and arguments.transform_file is None:
		#From the command line
		transformStr = arguments.transform
	else:
		print('ERROR: Specify either a transform file or a transform')
		return 1

	transformData = json.loads(transformStr)

	#Read the JSON in from stdin
	#TODO: error handling
	data = json.loads(sys.stdin.read())

	#Transform the JSON
	import Interpreter
	result = Interpreter.transformJson(data, transformData)

	#Output the result
	print(json.dumps(result, indent=arguments.indent, sort_keys=True))

	return 0

if __name__ == '__main__':
	sys.exit(main())
