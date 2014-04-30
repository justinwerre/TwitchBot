import unittest
import FileHandler

class TestFileHandler(unittest.TestCase):
	def setUp(self):
		self.fh = FileHandler.FileHandler()

	def tearDown(self):
		del self.fh

	def testParseUsername(self):
		options = self.fh.getOptions("testconfig.ini")
		self.assertEqual(options['nickname'], "username")

	def testParseOauth(self):
		options = self.fh.getOptions("testconfig.ini")
		self.assertEqual(options['oauth'], "token")

if __name__ == '__main__':
	unittest.main()