
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
