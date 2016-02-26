
def extractPath(data, path):
	splitPath = path.split('.')
	return extractSplitPath(data, splitPath)

def extractSplitPath(data, splitPath):
	nextData = data.get(splitPath[0])
	return nextData if len(splitPath) <= 1 or nextData is None else extractSplitPath(nextData, splitPath[1:])