
import base64
import binascii
import hashlib
import math

def maybe(f):
	return lambda *args: f(*args) if None not in args else None

def toBool(data):
	return data == 'True' or data == 'true'

def toFloat(data):
	try:
		return float(data)
	except ValueError:
		return None
	except TypeError:
		return None

def toInt(data):
	try:
		return int(data)
	except ValueError:
		return None
	except TypeError:
		return None

def toNumber(data):
	intValue = toInt(data)
	if intValue is not None:
		return intValue

	return toFloat(data)

def hashFunction(hashConstructor):
	def f(s):
		h = hashConstructor()
		h.update(s.encode('utf8', 'ignore'))
		return binascii.hexlify(h.digest()).decode('utf8')
	return f

functions = {
	#Any
	'toString': str,
	'toBool': toBool,
	'toFloat': toFloat,
	'toInt': toInt,
	'toNumber': toNumber,

	'abs': maybe(abs),

	#None
	'isNull': lambda x: x is None,

	'default': lambda x, y: x if x is not None else y,
	'defaultNan': lambda x: x if x is not None else float('nan'),

	#Bool
	'not': maybe(lambda x: not x),

	#Dict
	'keys': maybe(lambda d: list(d.keys())),
	'values': maybe(lambda d: list(d.values())),

	#Float
	'isFinite': maybe(lambda x: math.isfinite(x)),
	'isNan': maybe(lambda x: math.isnan(x)),

	'ceil': maybe(lambda x: math.ceil(x)),
	'cos': maybe(lambda x: math.cos(x)),
	'cosh': maybe(lambda x: math.cosh(x)),
	'erf': maybe(lambda x: math.erf(x)),
	'exp': maybe(lambda x: math.exp(x)),
	'floor': maybe(lambda x: math.floor(x)),
	'lg': maybe(lambda x: math.log2(x)),
	'ln': maybe(lambda x: math.log(x)),
	'log': maybe(lambda x: math.log10(x)),
	'sin': maybe(lambda x: math.sin(x)),
	'sinh': maybe(lambda x: math.sinh(x)),
	'sqrt': maybe(lambda x: math.sqrt(x)),
	'tan': maybe(lambda x: math.tan(x)),
	'tanh': maybe(lambda x: math.tanh(x)),

	#Int

	#Numer
	'+': maybe(lambda x, y: x + y),
	'-': maybe(lambda x, y: x - y),
	'*': maybe(lambda x, y: x * y),
	'/': maybe(lambda x, y: x / y),
	'**': maybe(lambda x, y: x ** y),
	'%': maybe(lambda x, y: x % y),

	'==': maybe(lambda x, y: x == y),
	'!=': maybe(lambda x, y: x != y),
	'<': maybe(lambda x, y: x < y),
	'<=': maybe(lambda x, y: x <= y),
	'>': maybe(lambda x, y: x > y),
	'>=': maybe(lambda x, y: x >= y),

	#Sequence
	'length': maybe(len),

	'first': lambda s: s[0] if s is not None and len(s) > 1 else None,
	'rest': lambda s: s[1:] if s is not None and len(s) > 1 else None,
	'last': lambda s: s[-1] if s is not None and len(s) > 1 else None,
	'init': lambda s: s[:-1] if s is not None and len(s) > 1 else None,

	'sorted': maybe(lambda s: list(sorted(s))),
	'unique': maybe(lambda s: list(set(s))),

	'sum': maybe(sum),
	#TODO: average
	#TODO: stddev
	#TODO: statistics

	'min': maybe(min),
	'max': maybe(max),

	'count': maybe(lambda s, f: s.count(f)),

	#String
	'lower': maybe(lambda s: s.lower()),
	'upper': maybe(lambda s: s.upper()),
	'capitalize': maybe(lambda s: s.capitalize()),
	'swapCase': maybe(lambda s: s.swapcase()),

	'strip': maybe(lambda s: s.strip()),
	'lstrip': maybe(lambda s: s.lstrip()),
	'rstrip': maybe(lambda s: s.rstrip()),

	'find': maybe(lambda s, f: s.find(f)),
	'replace': maybe(lambda s, f: s.replace(f)),
	'startsWith': maybe(lambda s, f: s.startswith(f)),
	'endsWith': maybe(lambda s, f: s.endswith(f)),

	'join': lambda s, *args: (args[0] if len(args) > 0 else '').join(s) if s is not None else None,
	'split': maybe(lambda s, sp: s.split(sp)),
	'lines': maybe(lambda s: s.split('\n')),
	'unlines': maybe(lambda s: '\n'.join(s)),
	'words': maybe(lambda s: s.split(' ')),
	'unwords': maybe(lambda s: ' '.join(s)),

	#Hashing
	'md5': hashFunction(hashlib.md5),
	'sha1': hashFunction(hashlib.sha1),
	'sha224': hashFunction(hashlib.sha224),
	'sha256': hashFunction(hashlib.sha256),
	'sha384': hashFunction(hashlib.sha384),
	'sha512': hashFunction(hashlib.sha512),
}
