
import json

import Utility

def parseTransform(transform):
	"""
	Parses a single JTL transform into tokens.

	:param transform: str
	:return: [[str]]
	"""
	#TODO: more robust parsing
	return [
		[token for token in tokens.split(' ') if token != '']
		for tokens in transform.split('$')
	]

def parseArgument(argument, data):
	"""
	Parses an argument to an operation.

	:param argument: str from tokenization
	:param data: dict of original data to extract more fields from
	:return: a valid JSON value
	"""
	try:
		#Try loading as a constrant first
		#TODO: strings are awkward and require escaping, so figure that out
		return json.loads(argument)
	except ValueError:
		#If that fails, it might be a name
		return Utility.extractPath(data, argument)
