from praw import errors,Reddit
from requests.exceptions import HTTPError, RequestException, MissingSchema, InvalidURL
import random
import config
import datetime

class RedditLink:
	def __init__(self,parent):
		self.r=Reddit(user_agent="PollBotBestBot")
		self.parent=parent
		self.messagable=True
		self.trackable=False
		self.active=True
		
	def help(self,admin):
		if self.active:
			return "!r/[subredditname] - return random result from a subreddit\n"
		return ""
		
	def message(self,msg,admin):
		if self.active:
			if msg["body"].lower().startswith("!r/"):
				m=msg["body"].lstrip("!r/")
				spli=m.split(":")
				subreddit=spli[0]
				if subreddit in config.banned_subreddits:
					self.parent.send_message(mto=self.parent.channel,mbody="Nope, not touching that.",mtype="groupchat")
					return
						
				body=self.get_hot(subreddit,msg)
				if body!=None:
					self.parent.send_message(mto=self.parent.channel,mbody=body,mtype="groupchat")
			
			if msg["body"].lower().startswith("!block ") and msg["mucnick"] in config.admins:
				m=m.spli(" ")
				subreddit=spli[1]
				config.banned_subreddits.append(subreddit)
			
	def get_hot(self,subreddit,msg):
		if msg["type"]=="groupchat":
			subreddit=self.r.get_subreddit(subreddit)
			try:
				if subreddit.over18:
					pass
			except (HTTPError, errors.InvalidSubreddit) as E:
				self.parent.send_message(mto=self.parent.channel,mbody="Learn to Reddit please, "+msg["mucnick"],mtype="groupchat")
				return None
				
			if subreddit.over18:
				#self.parent.send_message(mto=self.parent.channel,mbody="NSFW content is currently blocked. Direct complaints to mods and admins.",mtype="groupchat")
				extra=" :nws: "
			else:
				extra=""
				
			submissions=subreddit.get_hot(limit=10)
			a=None
			a1=None
			limit=random.randint(0,9)
			while limit>0:
				a1=a
				try:
					a=next(submissions)
				except StopIteration:
					a=a1
					break
				limit-=1
			
			try:
				return "\n"+extra+str(a.title)+extra+"\n"+extra+str(a.url)+extra
			except AttributeError:
				return "Reddit API is currently not accepting connections. Please wait ~30 seconds before retrying."