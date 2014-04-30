import configparser

class FileHandler:
	def __init__(self):
		self.temp = "just some filler code"

	def getOptions(self, fileName):
		config = configparser.ConfigParser()
		config.read(fileName)
		return config['ircsettings']
