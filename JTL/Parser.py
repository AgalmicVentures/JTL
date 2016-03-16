
import json
import shlex

import Utility

def parseTransform(transform):
	"""
	Parses a single JTL transform into tokens.

	:param transform: str
	:return: [[str]]
	"""
	#Create a lexer with some slight tweaks
	lexer = shlex.shlex(transform, posix=False)
	lexer.wordchars += '.+-'

	#Split into operations
	operations = []
	operation = []
	for token in lexer:
		#Split tokens on $
		if token == '$':
			operations.append(operation)
			operation = []
		else:
			operation.append(token)

	#Append any final operation
	operations.append(operation)

	return operations

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
