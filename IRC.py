import socket

class ircClient:
	def __init__(self, options):
		self.options = options

	def connect(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((self.options['server'], int(self.options['port'])))
		self.send('PASS ' + self.options['oauth'] + '\r\n')
		self.send('USER ' + self.options['nickname'] + ' 0 * :' + self.options['owner'] + '\r\n')
		self.send('NICK ' + self.options['nickname'] + '\r\n')
		self.send('JOIN ' + self.options['channel'] + '\r\n')

	def disconnect(self):
		self.irc.close()

	def recive(self):
		temp = self.irc.recv(1024)
		self.displayMessage(temp)

	def send(self, msg):
		self.irc.send(bytes(msg, 'UTF-8'))

	def privateMessage(self, msg):
		self.send("PRIVMSG " + self.options['channel'] + " :" + msg)

	def displayMessage(self, msg):
		sMsg = msg.decode('UTF-8')
		msgList = sMsg.splitlines()
		for strn in msgList:
			if 'PING' in strn:
				self.pong(strn)
			else: 
				print(strn)

	def pong(self, msg):
		tokens = msg.split()
		self.send('PONG ' + tokens[1])
		