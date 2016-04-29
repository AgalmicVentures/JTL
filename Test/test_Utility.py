
import datetime
import unittest

from JTL import Utility

class UtilityTest(unittest.TestCase):

	def setUp(self):
		self._testData = {
			'a': {
				'X': 3,
				'Y': 2,
			},
			'b': {'p': {'d': {'q': 'test'}}},
			'c': 'asdf',
		}

	def test_extractPath(self):
		self.assertEqual(Utility.extractPath(self._testData, 'a'), {'X': 3, 'Y': 2})
		self.assertEqual(Utility.extractPath(self._testData, 'a.X'), 3)
		self.assertEqual(Utility.extractPath(self._testData, 'a.Z'), None)
		self.assertEqual(Utility.extractPath(self._testData, 'b.p.d.q'), 'test')
		self.assertEqual(Utility.extractPath(self._testData, 'c'), 'asdf')

	def test_extractSplitPath(self):
		self.assertEqual(Utility.extractSplitPath(self._testData, ['a']), {'X': 3, 'Y': 2})
		self.assertEqual(Utility.extractSplitPath(self._testData, ['a', 'X']), 3)
		self.assertEqual(Utility.extractSplitPath(self._testData, ['a', 'Z']), None)
		self.assertEqual(Utility.extractSplitPath(self._testData, ['b', 'p', 'd', 'q']), 'test')
		self.assertEqual(Utility.extractSplitPath(self._testData, ['c']), 'asdf')
