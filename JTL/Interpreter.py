
import Functions
import Parser
import Utility

def applyOperation(value, operation, args):
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
		if len(args) == 0 and operation[0] == '.':
			return Utility.extractPath(value, operation[1:])

		#Nothing found -- error!
		raise NameError(operation)

	return function(value, *args)

def transform(data, transform):
	"""
	Computes one single transformation on some input data.

	:param data: dict
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
			raise SyntaxError('missing operation after: %s' % (tokens[n][0]))

		operation = section[0]
		args = [Parser.parseArgument(argument, data) for argument in section[1:]]
		value = applyOperation(value, operation, args)

	return value

def transformJson(data, transformData):
	"""
	Transforms some input data based on a transformation (transformData).

	:param data: dict
	:param transformData: dict | list | str
	:return: dict
	"""
	if type(transformData) is dict:
		result = {}
		for k, v in transformData.items():
			result[k] = transformJson(data, v)
	elif type(transformData) is list:
		result = [transformJson(data, v) for v in transformData]
	elif type(transformData) is str:
		result = transform(data, transformData)
	else:
		result = None
	return result
