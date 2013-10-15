import random
import config


class Shibe:
	def __init__(self,parent):
		self.parent=parent
		self.ignored_phrases=["",
							  "\t",
			                  "\n"]
		self.messagable=True
		self.trackable=False
		
		self.active=True
		
	def help(self,admin):
		if self.active:
			return "!shibe [thing 1] [thing 2] ... [thing N] - shibefy text\n"
			
	def shibefy(self,text):
		# Here is the function that actually shibefies
				
		l=["very",
		   "so",
		   "much",
		   "such"]
		   
		l2=[None]
		
		maxLength=min(8,len(text))
		wowCount=0
		dWowCount=random.randint(int(len(text)**0.5),int(len(text)))
		wows=[]
		for i in range(dWowCount):
			r=random.randint(0,len(text)+dWowCount-2)
			while r in wows and r-1 in wows and r+1 in wows:
				r=random.randint(0,len(text)+dWowCount-2) 
			wows.append(r)
		   
		sA=""
		runCount=0
		while len(text)>0:
			if len(l2)>maxLength:
				del l2[random.randint(1,len(l2)-1)]
			r=None
			while r in l2:
				r=random.randint(0,8)+2
			l2.append(r)
			s=""
			for j in range(r):
				s+="\t"
			if not runCount in wows:
				sA+="\n"+s+random.choice(l)+" "+text.pop(0)
			else:
				sA+="\n"+s+"wow"
			runCount+=1
		return sA
		 
	def message(self,msg,admin):
		if self.active:
			if msg["body"].startswith("!shibe ") and not msg["mucnick"] in config.excluded:
				
				# Separate the words to be shibefied
				
				spli=msg["body"].split(" ")
				
				del spli[0]
				if spli[0].lower()=="everyone" and msg["type"]=="chat":
					spli=self.parent.jidList.keys()
					
				a=0
				while a<len(spli):
					if spli[a] in self.ignored_phrases or spli.count(spli[a])>1:
						del spli[a]
					else:
						a+=1
				
				random.shuffle(spli)
						
				sA=self.shibefy(spli)
				
				if msg["type"]=="groupchat":
					self.parent.channel_message(sA)
				else:
					self.parent.private_message(msg["from"],sA)