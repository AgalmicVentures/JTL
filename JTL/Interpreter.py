
# Copyright (c) 2015-2023 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from JTL import Functions
from JTL import Parser
from JTL import Utility

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

def transform(data, transform, location=''):
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
