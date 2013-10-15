class Sajuuk:
	def __init__(self,parent):
		self.parent=parent
		
		self.messagable=True
		self.trackable=False
		
		self.active=True
		
	def help(self,admin):
		if self.active:
			return "!sajuuk - All glory to the hypno-Sajuuk\n"
			
	def message(self,msg,admin):
		if self.active:
			if msg["body"].lower().startswith("!sajuuk"):
				
				if msg["type"]=="groupchat":
					self.parent.channel_message("SAJUUK - GLORIOUS LEADER OF TRYRM (Also, Supcom player)")
				elif msg["type"]=="chat":
					self.parent.private_message("SAJUUK - GLORIOUS LEADER OF TRYRM (Also, Supcom player)")
		