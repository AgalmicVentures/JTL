
import Functions
import Parser
import Utility

def applyOperation(value, operation, args, location):
	"""
	Applies an operation to a value with some extra arguments.

	:param value: a valid JSON value
	:param operation: str name of the operation to apply (from the tokenizer)
	:param args: [str] argument tokens
	:return: a valid JSON value
	"""
	function = Functions.functions.get(operation)
	if function is None:
		#Is it a simple integer index?
		index = Functions.toInt(operation)
		if index is not None:
			return value[index]

		#Or perhaps it's a selector function? .abc.def
		if operation[0] == '.':
			if len(args) == 0:
				return Utility.extractPath(value, operation[1:])
			else:
				raise SyntaxError('selector  %s  has arguments in "%s" (did you mean to do an operation?)' % (operation[0], location))

		#Nothing found -- error!
		raise NameError('cannot find operation  %s  in "%s"' % (operation, location))

	return function(value, *args)

def transform(data, transform, location):
	"""
	Computes one single transformation on some input data.

	:param data: dict
	:param key: str output key (used for error reporting)
	:param transform: str JTL expression
	:return: a valid JSON value
	"""
	#Parse the transformation into tokens
	tokens = Parser.parseTransform(transform)
	if len(tokens) == 0:
		return None

	primarySelector = tokens[0][0]
	value = Utility.extractPath(data, primarySelector)
	for n, section in enumerate(tokens[1:]):
		if len(section) == 0:
			#n is the previous token
			raise SyntaxError('missing final operation after  %s  in "%s"' % (tokens[n][0], location))

		operation = section[0]
		args = [Parser.parseArgument(argument, data) for argument in section[1:]]
		value = applyOperation(value, operation, args, location)

	return value

def transformJson(data, transformData, location=''):
	"""
	Transforms some input data based on a transformation (transformData).

	:param data: dict
	:param transformData: dict | list | str
	:return: dict
	"""
	if type(transformData) is dict:
		result = {}
		for k, v in transformData.items():
			result[k] = transformJson(data, v, '%s.%s' % (location, k))
	elif type(transformData) is list:
		result = [transformJson(data, v, '%s.%s' % (location, n)) for n, v in enumerate(transformData)]
	elif type(transformData) is str:
		result = transform(data, transformData, location)
	else:
		result = None
	return result
