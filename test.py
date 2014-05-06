import FileHandler
import IRC

fh = FileHandler.FileHandler()
options = fh.getOptions("twitch.ini")
chat = IRC.ircClient(options)
chat.connect()
while True:
	chat.recive()
chat.disconnect()