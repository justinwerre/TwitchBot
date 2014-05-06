import unittest
import FileHandler

class TestFileHandler(unittest.TestCase):
	def setUp(self):
		self.fh = FileHandler.FileHandler()
		self.options = self.fh.getOptions("testconfig.ini")

	def tearDown(self):
		del self.fh

	def testParseUsername(self):
		self.assertEqual(self.options['nickname'], "username")

	def testParseOauth(self):
		self.assertEqual(self.options['oauth'], "token")

	def testParseChannel(self):
		self.assertEqual(self.options['channel'], 'testchannel')

	def testParseServer(self):
		self.assertEqual(self.options['server'], 'testserver')

	def testParsePort(self):
		self.assertEqual(int(self.options['port']), 1234)

if __name__ == '__main__':
	unittest.main()