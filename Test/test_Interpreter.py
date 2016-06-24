
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

	def test_transformChain(self):
		self.assertEqual(Interpreter.transform(self._testData, 'a.X'), 3)
		self.assertEqual(Interpreter.transform(self._testData, 'a $ .X'), 3)
		self.assertEqual(Interpreter.transform(self._testData, 'a $ .X $ toString'), "3")

	def test_transformArithmetic(self):
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ + a.Y'), 5)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ - a.Y'), 1)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ * a.Y'), 6)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ / a.Y'), 1.5)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ % a.Y'), 1)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ ** a.Y'), 9)

	def test_transformComparison(self):
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ == 3'), True)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ != 3'), False)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ >= 3'), True)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ > 3'), False)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ <= 3'), True)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ < 3'), False)
		self.assertEqual(Interpreter.transform(self._testData, 'a.X $ == 3 $ not'), False)

	def test_transformDictionary(self):
		self.assertEqual(Interpreter.transform(self._testData, 'a $ keys $ sorted'), ['X', 'Y'])
		self.assertEqual(Interpreter.transform(self._testData, 'a $ values $ sorted'), [2, 3])
