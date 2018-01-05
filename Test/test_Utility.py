
# Copyright (c) 2015-2018 Agalmic Ventures LLC (www.agalmicventures.com)
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
