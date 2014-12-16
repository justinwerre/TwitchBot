import CustomExceptions
import socket
import re

class ircClient:
	def __init__(self, options):
		self.options = options
		self.data = ''
		self.run = True

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
		self.data += self.irc.recv(1024).decode('UTF-8')
		self.handleMessage()

	def send(self, msg):
		self.irc.send(bytes(msg, 'UTF-8'))

	def privateMessage(self, msg):
		self.send("PRIVMSG " + self.options['channel'] + " :" + msg)

	def handleMessage(self):
		msgList = self.data.splitlines()
		for strn in msgList:
			if 'PING' in strn:
				self.pong(strn)
			else: 
				#try and parse a user message from the strn
				try:
					msg = self.parseMessage(strn)
					print(msg['username'] + ": " + msg['message'])
					self.checkCommand(msg)
				#if there is no user message, just print out the line
				except IndexError:
					print(strn)
		#don't forget to clear out data that we've already delt with
		self.data = '';

	# replies to a ping message
	def pong(self, msg):
		tokens = msg.split()
		self.send('PONG ' + tokens[1])

	#parse out the username and message from the line
	#regulare expressions from: https://github.com/aidraj/twitch-bot/blob/master/src/lib/irc.py
	def parseMessage(self, msg):
		return{
			'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', msg)[0],
			'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', msg)[0]
		}
		
	#check if the message is a command and the user has permission to perform that command
	def checkCommand(self, msg):
		if msg['username'] == self.options['owner']:
			commands = msg['message'].split(' ')
			for command in commands:
				print(command)
				if(command == '!exit'):
					self.run = False
