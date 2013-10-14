import chatlings
import threading

import sleekxmpp

import inspect
import sys

import ssl

import config

class ModularBot(sleekxmpp.ClientXMPP):
	def __init__(self, jid, password, nick, channel):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self.jid = jid
		self.password = password
		self.nick = nick
		self.channel = channel
		
		self.callLock=threading.Lock()
		self.callables={}
		
		self.trackLock=threading.Lock()
		self.trackables={}
		
		self.load_modules()

		#self.add_event_handler("groupchat_presence", self.updateJIDs)
		self.add_event_handler("session_start", self.start)
		self.add_event_handler("message", self.call_handler)
		
	def load_modules(self):
		
		for i in chatlings.classDictionary:
			real_thing=chatlings.classDictionary[i](self)
			print real_thing
			
			if real_thing.callable:
				self.callables[i]=real_thing
			if real_thing.trackable:
				self.trackables[i]=real_thing
					

			
		print self.callables
		print self.trackables
		
	def start(self):
		self.send_presence()
		r=self.get_roster()
		self.plugin['xep_0045'].joinMUC(self.channel, self.nick, wait=False)
		
	def call_handler(self,msg):
		
		self.callLock.acquire()
		if msg["type"]=="chat":
			if msg["from"] in config.admins:
				if msg["body"].lower().startswith("!load"):
					self.load(msg["body"])
		
		for i in self.callables:
			callable=self.callables[i]
			callable(msg)
		self.callLock.release()
		
			
	def track_handler(self):
		self.trackLock.acquire()
		try:
			self.trackerLock.acquire()
			i=self.trackers.pop(0)
			i()
			self.trackers.append(i)
				
			self.LastFM()
			self.trackerLock.release()
		finally:
			pass
		self.trackLock.release()
			
	def load(self,name):
		if name in chatlings.modules.keys():
			module=chatlings.modules[name]
			
			if module.callable:
				self.callLock.acquire()
				self.callables[name]=module.add(self)
				self.callLock.release()
			if module.trackable:
				self.trackLock.acquire()
				self.trackables[name]=module.add(self)
				self.trackLock.release()
				
	def channel_message(self,content):
		self.send_message(mto=self.channel,mbody=content,mtype="groupchat")
		
	def private_message(self,user,content):
		self.send_message(mto=user,mbody=content,mtype="groupchat")
		
mb=ModularBot(config.jid,config.password,"ModularBot",config.channel)
mb.register_plugin('xep_0030')	 # Service discovery.
mb.register_plugin('xep_0045')	 # MUC support.
mb.register_plugin('xep_0199')	 # XMPP Ping
mb.ssl_version = ssl.PROTOCOL_SSLv3

if mb.connect((config.server,5222)):
	mb.process(block=True)
else:
	print "Failed to connect."
	exit()
		