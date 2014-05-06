import configparser

class FileHandler:
	def getOptions(self, fileName):
		config = configparser.ConfigParser()
		config.read(fileName)
		return config['ircsettings']
