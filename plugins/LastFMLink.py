import pylast

class LastFMLink:
	def __init__(self,parent):
		self.parent=parent
		self.tracked=[]
		
		self.active=True
		
		self.trackable=True
		self.messagable=True
		
		self.authenticate()
		
	def emote_clean(self,s):
		new_s=""
		b=True
		for i in s:
			if i==":":
				b=not b
			if b and i!=":":
				new_s+=i
		return new_s
		
	def jid2nick(self,jid):
		return str(jid).split("@")[0]
		
	def authenticate(self):
		api_key="7813db7c21ddbca72445e30e6b3fe5e3"
		api_secret="e823daf4c89db91f55c7a7f4aa3b2da7"
		
		username = "Syreniac"
		password_hash = pylast.md5("dc53HeUp")
		
		self.network = pylast.LastFMNetwork(api_key=api_key,
											api_secret=api_secret,
											username=username,
											password_hash=password_hash)
		
	def track_user(self,user,jName):
		for i in self.tracked:
			if i[0]==jName:
				return
		self.tracked.append([jName,self.network.get_user(user),None])
		
	def help(self,admin):
		if self.active:
			return "!lastfm [name] - If sent in PM, tracks your account [name] on Last.FM\n"
		return ""
		
	def message(self,msg,admin):
		if msg["type"]=="chat":
			
			if msg["body"].lower().startswith("!lastfm "):
				try:
					s=msg["body"].split(" ")[1]
					self.track_user(s,msg["mucnick"])
				except IndexError:
					pass
		
										
	def check_user(self,user_data):
		try:
			new_track=user_data[1].get_now_playing()
			if not new_track is None:
				if new_track.title!=user_data[2]:
					title=self.emote_clean(new_track.title)
					user_data[2]=title
					self.parent.channel_message(user_data[0]+" has started listening to "+str(title)+" by "+str(new_track.artist))
		except IndexError:
			pass
										
	def track(self):
		if self.active:
			if len(self.tracked)>0:
				user_data=self.tracked.pop(0)
				try:
					self.check_user(user_data)
				except:
					pass
				self.tracked.append(user_data)