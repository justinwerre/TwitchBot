import configparser

class FileHandler:
	#parse the ini file and return the results object
	def getOptions(self, fileName):
		config = configparser.ConfigParser()
		config.read(fileName)
		return config
