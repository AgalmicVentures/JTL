
import datetime
import unittest

from JTL import Functions

class FunctionsTest(unittest.TestCase):

	def setUp(self):
		self._testData = {
			'a': {
				'X': 1,
				'Y': 2,
			},
			'b': {'p': {'d': {'q': 'test'}}},
			'c': 'asdf',
		}

	def test_toBool(self):
		self.assertEqual(Functions.toBool('True'), True)
		self.assertEqual(Functions.toBool('true'), True)

		self.assertEqual(Functions.toBool('False'), False)
		self.assertEqual(Functions.toBool('false'), False)

		self.assertEqual(Functions.toBool('t'), False)
		self.assertEqual(Functions.toBool('y'), False)

	def test_toInt(self):
		self.assertEqual(Functions.toInt('1'), 1)
		self.assertEqual(Functions.toInt('0'), 0)
		self.assertEqual(Functions.toInt('-1'), -1)

		self.assertEqual(Functions.toInt('1.1'), None)
		self.assertEqual(Functions.toInt(1.1), 1)

	def test_toNumber(self):
		self.assertEqual(Functions.toNumber('1'), 1)
		self.assertEqual(Functions.toNumber('0'), 0)
		self.assertEqual(Functions.toNumber('-1'), -1)

		self.assertEqual(Functions.toNumber('1.1'), 1.1)
		self.assertEqual(Functions.toNumber(1.1), 1.1)
