
def extractPath(data, path):
	"""
	Indexes a JSON object with a period separated path.

	:param data: dict
	:param path: str
	:return: a valid JSON value
	"""
	splitPath = path.split('.')
	return extractSplitPath(data, splitPath)

def extractSplitPath(data, splitPath):
	"""
	Indexes a JSON object with list of string keys as a path.

	:param data: dict
	:param path: [str]
	:return: a valid JSON value
	"""
	nextData = data.get(splitPath[0])
	return nextData if len(splitPath) <= 1 or nextData is None else extractSplitPath(nextData, splitPath[1:])
