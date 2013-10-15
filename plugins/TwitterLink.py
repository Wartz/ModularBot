from twitter import Api
import re

CONSUMER_KEY="GzdwGVOhtFkBopVz5cdlwg"
CONSUMER_SECRET="ncB8WRtNuhWfToDoWolRGb2q7pMfrV49uC1o7iWC9Y"
ACCESS_KEY="625637844-KgQRSLyNOSFRyYREwBtD41IKAsavNdmklxg4jSoo"
ACCESS_SECRET="2PlKswAKVYKT6VUxSkKKpgMgCIpTStvbPXjp9ocnQ"

def remove_hashtags(s):
	new_s=""
	b=True
	for i in s:
		if i=="#":
			b=False
		if b:
			new_s+=i
		elif not re.match("^[\w\d]*$",i) and i!="#":
			b=True
	a=-1
	return new_s
		

class TwitterLink:
	def __init__(self,parent):
		self.parent=parent
		
		self.targets={}
		self.target_names=[]
		
		self.messagable=True
		self.trackable=True
		
		self.active=True
		
		self.api = Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
						access_token_key=ACCESS_KEY, access_token_secret=ACCESS_SECRET)
						
		print "hello"
		
		
	def help(self,admin):
		if self.active:
			if admin:
				return "!twittertrack [name] [keywords] - track the name on twitter when they tweet with the keywords\n!twitteruntrack [name] - stop tracking the name on twitter"
		return ""
		
	def load_file(self,target):
		try:
			f=open(target+".txt","r")
			r=f.read().split("\n")
			a=0
			while a<len(r):
				if r[a]=="":
					del r[a]
				else:
					a+=1
			old_tweet=r[-1]
			f.close()
		except IOError:
			print "IOError"
			f=file(target+".txt","w+")
			f.write("")
			f.close()
			old_tweet=""
		except IndexError:
			print "IndexError"
			old_tweet=""
			
		self.target_names.append(target)
		self.targets[target]=[0,0,0]
		self.targets[target][0]=""
		self.targets[target][1]=open(target+".txt","a+")
		self.targets[target][2]=old_tweet

	def FetchTwitter(self,target,limit=1):
		statuses = self.api.GetUserTimeline(screen_name="@"+target, count=limit)
		s=str(statuses[limit-1].text)
		print s
		return s
		
	def message(self,msg,admin):
		if msg["type"]=="chat" and self.active:
			
			if msg["body"].startswith("!twittertrack "):
				split=msg["body"].split(" ")
				try:
					name=split[1]
				except IndexError:
					return
				try:
					keywords=split[2].split(",")
				except IndexError:
					keywords=""
				self.targets[name]=[keywords,None,None]
				self.load_file(name)
				
			if msg["body"].startswith("!twitteruntrack "):
				split=msg["body"].split(" ")
				try:
					name=split[1]
				except IndexError:
					return
				
				del self.targets[name]
				self.target_names.remove(name)
				
			
	def track(self):
		if self.active:
			print self.target_names
			print self.targets
			if self.target_names!=[] and self.active:
				target_name=self.target_names.pop(0)
				target=self.targets[target_name]
				self.target_names.append(target_name)
				try:
					new_tweet=self.FetchTwitter(target_name)
				except:
					return
					
				new_tweet=remove_hashtags(new_tweet)
				write_tweet=new_tweet+"\n"

				limit=1
				while str(target[2])!=str(new_tweet) and target[2]!="":
					limit+=1
					maybe_new_tweet=self.FetchTwitter(target_name,limit)
			
					maybe_new_tweet=remove_hashtags(maybe_new_tweet)
						
						
					if str(maybe_new_tweet)==str(target[2]):
						break
					else:
						new_tweet=maybe_new_tweet
				print new_tweet

				if str(target[2])!=str(new_tweet):
					if target[0]!="":
						for i in target[0]:
							if not i in new_tweet:
								return
					target[1].write(write_tweet)
					target[1].flush()
					target[2]=new_tweet
					self.parent.channel_message("@"+target_name+"\n\t"+new_tweet)