import plugins
import threading

import logging

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
		
		self.lock=threading.Lock()
		self.messagables={}
		
		self.trackables={}
		
		self.jidList={}
		
		self.load_modules()

		self.add_event_handler("groupchat_presence", self.updateJIDs)
		self.add_event_handler("session_start", self.start)
		self.add_event_handler("message", self.msg_handler)
		
		self.scheduler.add("Tracking",5.0,self.track_handler,repeat=True)
		
	def updateJIDs(self,msg):
		if msg["type"]=="available":
			if not msg["mucnick"] in self.jidList.keys():
				self.jidList[msg["mucnick"]]=True
		elif msg["type"]!="subscribe":
			print "REMOVING "+msg["mucnick"]+":"+str(msg["type"])
			if msg["mucnick"] in self.jidList:
				del self.jidList[msg["mucnick"]]
				
		print "-------------------"
			
		
	def load_modules(self):
		
		for i in plugins.classDictionary:
			real_thing=plugins.classDictionary[i](self)
			print real_thing
			
			if real_thing.messagable:
				self.messagables[i]=real_thing
			if real_thing.trackable:
				self.trackables[i]=real_thing
		
	def start(self,arg):
		self.send_presence()
		r=self.get_roster()
		self.plugin['xep_0045'].joinMUC(self.channel, self.nick, wait=False)
		self.plugin['xep_0045'].joinMUC(self.channel, self.nick, wait=False)
		
	def msg_handler(self,msg):
		
		self.lock.acquire()
		
		if msg["type"]=="chat":
			if msg["from"] in config.admins:
				if msg["body"].lower().startswith("!enable"):
					self.toggle(msg["body"][8:],False)
					self.channel_message(msg["body"][9:]+" enabled!")
				if msg["body"].lower().startswith("!disable"):
					self.toggle(msg["body"][9:],False)
					self.channel_message(msg["body"][9:]+" disabled!")
		
		for i in self.messagables:
			messagable=self.messagables[i]
			messagable.message(msg)
		self.lock.release()
		
			
	def track_handler(self):
		self.lock.acquire()
		for i in self.trackables:
			trackable=self.trackables[i]
			trackable.track()
		self.lock.release()
		
	def toggle(self,name,toggle):
		self.lock.acquire()
		if name in self.messagables:
			self.messagables[name].active=toggle
			
		if name in self.trackables:
			self.trackables[name].active=toggle
		self.lock.release()		
				
	def channel_message(self,content):
		self.send_message(mto=self.channel,mbody=content,mtype="groupchat")
		
	def private_message(self,user,content):
		self.send_message(mto=user,mbody=content,mtype="groupchat")
		
if __name__=="__main__":
	logging.basicConfig(format='%(levelname)-8s %(message)s')		
			
	mb=ModularBot(config.jid,config.password,config.nick,config.channel)
	mb.register_plugin('xep_0030')	 # Service discovery.
	mb.register_plugin('xep_0045')	 # MUC support.
	mb.register_plugin('xep_0199')	 # XMPP Ping
	mb.ssl_version = ssl.PROTOCOL_SSLv3

	if mb.connect((config.server,5222)):
		print "Attempting to connect"
		mb.process(block=True)
	else:
		print "Failed to connect."
		exit()
		