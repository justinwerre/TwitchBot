import CustomExceptions
import socket
import re

class ircClient:
	def __init__(self, options):
		self.options = options['ircsettings']
		self.commands = options['commands']
		self.data = ''
		self.run = True

	#connect to the irc server
	def connect(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((self.options['server'], int(self.options['port'])))
		self.send('PASS ' + self.options['oauth'] + '\r\n')
		self.send('USER ' + self.options['nickname'] + ' 0 * :' + self.options['owner'] + '\r\n')
		self.send('NICK ' + self.options['nickname'] + '\r\n')
		self.send('JOIN ' + self.options['channel'] + '\r\n')

	#disconnect from the irc server
	def disconnect(self):
		self.irc.close()

	#get a message from the irc server
	def recive(self):
		self.data += self.irc.recv(1024).decode('UTF-8')
		self.handleMessage()

	#send the message to the server
	def send(self, msg):
		self.irc.send(bytes(msg, 'UTF-8'))

	#format a string to to the correct form for a message to the irc server
	def privateMessage(self, msg):
		self.send("PRIVMSG " + self.options['channel'] + " :" + msg +'\r\n')

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
		print(tokens[1])
		self.send('PONG ' + tokens[1] + '\r\n')

	#parse out the username and message from the line
	#regular expressions from: https://github.com/aidraj/twitch-bot/blob/master/src/lib/irc.py
	def parseMessage(self, msg):
		return{
			'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', msg)[0],
			'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', msg)[0]
		}
		
	#check if the message is a command and the user has permission to perform that command
	def checkCommand(self, msg):
		command = msg['message'].split(' ')[0]
		print(command)
		if msg['username'] == self.options['owner']:
			if command == '!exit':
				self.run = False
		if command == '!commands':
			#print out the avalible commands
			commandString = 'Commands: ' + ', '.join(self.commands)
			self.privateMessage(commandString)
		else:
			for com in self.commands:
				print(com)
				if com == command:
					self.privateMessage(self.commands[com])