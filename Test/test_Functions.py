
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

from JTL import Functions

class FunctionsTest(unittest.TestCase):

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
