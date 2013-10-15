class Koahi:
	def __init__(self,parent):
		self.parent=parent
		
		self.messagable=True
		self.trackable=False
		
		self.active=True
		
	def help(self,admin):
		if self.active:
			return "!koahi - returns the laws of koahi\n"
			
	def message(self,msg,admin):
		if self.active:
			if msg["body"].lower().startswith("!koahi"):
				
				if msg["type"]=="groupchat":
					self.parent.channel_message("\nDo:\n\tBe Cool\n\tHave Fun\nDon't\n\tBe Uncool\n\tGet Butthurt")
				elif msg["type"]=="chat":
					self.parent.private_message(msg["from"],"\nDo:\n\tBe Cool\n\tHave Fun\nDon't\n\tBe Uncool\n\tGet Butthurt")
		
	