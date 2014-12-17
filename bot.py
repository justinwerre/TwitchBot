import FileHandler
import IRC

fh = FileHandler.FileHandler()
options = fh.getOptions("twitch.ini")
chat = IRC.ircClient(options)
chat.connect()
run = True
while chat.run:
	chat.recive()
chat.disconnect()