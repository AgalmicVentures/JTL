
import datetime
import unittest

from JTL import Interpreter

class InterpreterTest(unittest.TestCase):

	def setUp(self):
		self._testData = {
			'a': {
				'X': 3,
				'Y': 2,
			},
			'b': {'p': {'d': {'q': 'test'}}},
			'c': 'asdf',
		}

	def test_transform(self):
		self.assertEqual(Interpreter.transform(self._testData, 'a.X'), 3)
		self.assertEqual(Interpreter.transform(self._testData, 'a $ .X'), 3)
		self.assertEqual(Interpreter.transform(self._testData, 'a $ .X $ toString'), "3")

		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ + a.Y'), 5)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ - a.Y'), 1)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ * a.Y'), 6)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ / a.Y'), 1.5)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ % a.Y'), 1)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ ** a.Y'), 9)
