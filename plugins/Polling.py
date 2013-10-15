import random
import string
	
def getLetter(a,b=None):
	if b!=None:
		l=[]
		for i in string.lowercase[a:b]:
			l.append(i)
		return l
	else:
		return string.lowercase[a]
		
def endreplace(s,fs,rs):
	if s.endswith(fs):
		s=s[:-len(fs)]
		s+=rs
	return s
	
class Polling:
	def __init__(self,parent):
		self.parent=parent
		
		self.messagable=True
		self.trackable=False
		self.polling=True
		
		self.active=True
		
		self.polling=0
		
		self.tiebreaker="Eurobot"
		
	def help(self,admin):
		if self.active:
			return "!poll [option 1] or [option 2] ... or [option N] - start a poll with the options\n!pollover - stops a poll if you started one\n"
			
	def message(self,msg,admin):
		if self.active:
			if msg["type"]=="groupchat":
				if self.polling==1:
					m=msg["body"].lower()
					if msg["mucnick"]==self.pollStart or admin:
						if m.startswith("!pollover"):
							self.pollBreak()
					if m in self.pollkeys:
						if not msg["mucnick"] in self.polled:
							self.polled.append(msg["mucnick"])
							vote=ord(m[0]) - 97
							self.pollresults[vote]+=1
							
						else:
							sendString="No cheating please, "+str(msg["mucnick"])
							self.parent.channel_message(sendString)
				elif self.polling==-1:
					if msg["mucnick"]==self.tiebreaker:
						m=msg["body"].lower()
						if m in ["a","b"]:
							self.pollOver(m[0]=="a")
						else:
							self.polling=0
							self.parent.channel_message("Once again, Eurobot impresses me with its inability to make decisions")
				elif self.polling==0:
					if msg["body"].startswith("!poll"):
						
						
						m=msg["body"].lstrip("!poll")
						m=m.rstrip("?")
						if m[0]==" ":
							m=m[1:]
						
						m=m.split(" or ")
						
						if len(m)>1:
						
						
							sendString="Poll noted."
							
							self.pollresults=[]
							self.pollOptions=[]
							self.pollkeys=[]
							self.polled=[]
							a=0
							for i in m:
								
								sendString+="\n\t"+getLetter(a).upper()+": "+i
								self.pollOptions.append(i)
								self.pollresults.append(0)
								self.pollkeys.append(getLetter(a))
								a+=1
								
							sendString+="\n\t"+getLetter(a).upper()+": "+"checkbox"
							self.pollOptions.append("checkbox")
							self.pollresults.append(0)
							self.pollkeys.append(getLetter(a))
						
							
							sendString+="\nPlease enter your choices using the relevant letters."
								
							self.polling=1
							
							self.pollStart=msg["mucnick"]
							
							self.parent.scheduler.add("Poll",30.0,self.pollFunc,repeat=False)
					
							self.parent.channel_message(sendString)
						else:
							self.parent.channel_message("That poll is terrible, and I don't like it")
					

	def pollBreak(self):
		self.parent.scheduler.remove("Poll")
		self.pollOver()
		
	
		
	def tiebreak(self):
		s=""
		a=0
		for i in self.pollOptions:
			if self.pollresults[a]==max(self.pollresults):
				s+=i+" or "
			a+=1
		s=s[:-4]
		sendString=self.tiebreak+": TIEBREAK: "+s+"?"
		self.parent.channel_message(sendString)
		
	
	def pollFunc(self):
		self.pollOver()
		
	def pollOver(self,b=None):
		if self.polling!=0 or b!=None:
			if b==None:
				self.parent.channel_message("The poll is over!")
			self.polling=0
			
			c=0
			m=max(self.pollresults)
			for i in self.pollresults:
				if i==m:
					c+=1
			
			if c>1 and b==None:
				sendString="It's a tie!"
				self.polling=-1
				self.parent.scheduler.add("Tiebreak",1.0,self.tiebreak,repeat=False)
			else:
				ind=self.pollresults.index(m)
				
				if b!=None:
					sendString=self.pollOptions[ind]+" is the winner through "+self.tiebreaker+"'s decision!"
				else:
					sendString=self.pollOptions[ind]+" is the winner with "+str(self.pollresults[ind])+" votes!"
			

				
			self.parent.channel_message(sendString)