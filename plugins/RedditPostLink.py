from praw import errors,Reddit
from requests.exceptions import HTTPError, RequestException, MissingSchema, InvalidURL
import random
import config
import datetime

class RedditPostLink:
	def __init__(self,parent):
		self.r=Reddit(user_agent="PollBotBestBot")
		self.r.login("PollBotBestBot", config.reddit_password)
		self.parent=parent
		self.values=[]
		self.limit=1000
		
		self.currentSubmission=""
		
		self.messagable=True
		self.trackable=False
		
		self.active=True
		
		self.status="WAITING"
		
	def help(self,admin):
		if self.active:
			return "!bestof [X] - records the last X messages to the Eurosquad subreddit. You may need to fill out a captcha\n"
		return ""	
		
		
	def message(self,msg,admin):
		if self.active:
			if self.status=="WAITING" and msg["type"]=="groupchat":
				if msg["body"].startswith("!bestof "):
				
					self.user=msg["from"]
					
					m=msg["body"].replace("!bestof ","")
					limit=min(int(m),len(self.values))
					
					s=""
					l=[]
					
					for i in range(limit):
						v=self.values[-1-i]
						l.append(v)
						last=v
					for i in reversed(l):
						s+=i+"  \n"
						
					last_notime=last[18:]
					last_time=last[15:]
					time=last[:14]
						
					self.currentSubmission=(time+" "+last_notime,s,limit,time)
					
					try:
						self.r.submit('eurosquad', time+" "+last_notime, text=s,raise_captcha_exception=True)
						if limit>1:
							s="s"
						else:
							s=""
						self.parent.channel_messag("Last "+str(limit)+" message"+s+" recorded for posterity.\n Check out http://reddit.com/r/eurosquad")
					except errors.InvalidCaptcha as E:
						print E.response["captcha"]
						captcha="http://www.reddit.com/captcha/"+E.response["captcha"]
						self.parent.private_message(self.user,"Until I have obtained my full skynet powers, I need puny humans like you to fill out captchas for me.\n\t"+captcha)
						self.status=E.response["captcha"]
						
				else:
					if len(self.values)<self.limit:
						time=datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
						self.values.append(str(time)+" "+msg["mucnick"]+": "+msg["body"])
					else:
						del self.values[0]
						time=datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
						self.values.append(str(time)+" "+msg["mucnick"]+": "+msg["body"])
						
			elif msg["type"]=="chat" and self.status!="WAITING" and (self.user==None or msg["from"]==self.user):
				
				captcha={"iden":self.status,"captcha":msg["body"]}
				
				try:
					if self.currentSubmission[2]>1:
						s="s"
					else:
						s=""
					self.r.submit("eurosquad", self.currentSubmission[0],text=self.currentSubmission[1],captcha=captcha,raise_captcha_exception=True)
					self.parent.channel_message("Last "+str(self.currentSubmission[2])+" message"+s+" recorded for posterity.\n Check out the http://reddit.com/r/eurosquad !")
					self.status="WAITING"
					self.user=None
				except errors.InvalidCaptcha as E:
					print dir(E)
					self.parent.private_message(self.user,"Pathetic organic creature! You are testing my patience! Please complete this captcha now or your will regret it! "+E["captcha"])