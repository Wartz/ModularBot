import random

class FC:
	def __init__(self,parent):
		self.parent=parent
		
		self.messagable=True
		self.trackable=False
		self.polling=True
		
		self.active=True
		
		self.tiebreaker="Syreniac"
		
	def help(self,admin):
		if self.active:
			return "!fc - ask for FC advice\n"
			
	def message(self,msg,admin):
		if self.active:
			if msg["body"].lower().startswith("!fc"):
				if msg["type"]=="groupchat":
					self.parent.channel_message(self.FC())
				elif msg["type"]=="chat":
					self.parent.private_message(msg["from"],self.FC())
	
	def FC(self):
		commands=["Primary is %|",
				  "Secondary is %|",
				  "Don't shoot %",
				  "Shoot %",
				  "Burn towards %",
				  "Burn away from %",
				  "More bubbles on %",
				  "Get the bubbles off %",
				  "Flee for your lives from %",
				  "Oh god what even is $",
				  "Warp to %",
				  "Align to %",
				  "Web %",
				  "Tackle %",
				  "Scram %",
				  "Point %",
				  "Paint %",
				  "Damp %",
				  "Jam %",
				  "Stop DPS on %",
				  "More DPS on %",
				  "Scatter away from %",
				  "Starburst everywhere",
				  "Recite a terrible fanfic to %",
				  "Bump %",
				  "Don't bump %",
				  "Get reps on %",
				  "Stop reps on %",
				  "Reps aren't holding on %",
				  "Bring $",
				  "Don't bring $",
				  "Gate is Red",
				  "Gate is Green",
				  "Free burn",
				  "If you jump, you're dead",
				  "You jumped, didn't you?",
				  "Can I get { to scout?",
				  "Time to commissar %",
				  "RABBLE RABBLE RABBLE",
				  "CHECK CHECK CHECK",
				  "SHUT THE FUCK UP",
				  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
				  "Put gfs in local",
				  "Smack talk in local",
				  "Orbit $ at *",
				  "Keep % at Range at *",
				  "We're standing down",
				  "Does anyone have a perch?",
				  'Log in to Kugu and post "YOU GOT DUNKED"',
				  'Log in to Kugu and whine about blobs',
				  'Log in to Kugu and shitpost',
				  'Log in to Kugu and blame Goons',
				  "Don't worry PL will save us",
				  "Wait, why are they shooting us?",
				  "Wait, they're blues?",
				  "Who bombed the blues?",
				  "It's awoxing time!",
				  "Who's alt just awoxed?",
				  "SPAIS!!!!!!",
				  "We need more spies!",
				  "We need more #^",
				  "Why would we need more #^",
				  "~ ^ useless for this fleet",
				  "Anchor on me",
				  "Align to a random celestial",
				  "Hands are clean!",
				  "Cyno's up",
				  "Bridge, bridge, bridge",
				  "Jump, jump, jump",
				  "Diplos can deal with it",
				  ":frogsiren: Hostile supers tackled :frogsiren:",
				  ":frogsiren: FRIENDLY SUPERS TACKLED :frogsiren:",
				  "Ha, jokes on you, it's actually a structure shoot",
				  "Well, I've been poached by PL, see you round!",
				  "Well, I've been poached by DYS0N, see you later!",
				  "Well, I've been poached by EMP, see you later!",
				  "Well, I've been poached by Goons, see you later!",
				  "welp",
				  "VFK by []!",
				  "Was it %|? I bet it was %|",
				  ":getin:",
				  "But what about my killboard stats!?",
				  "Nobody cares about your killboard stats",
				  "Your killboard stats are terrible."]
				  
		targets=["Rifter",
				 "Burst",
				 "Slasher",
				 "Vigil",
				 "Breacher",
				 "Tristan",
				 "Incursus",
				 "Atron",
				 "Maulus",
				 "Navitas",
				 "Merlin",
				 "Kestrel",
				 "Condor",
				 "Griffin",
				 "Bantam",
				 "Punisher",
				 "Inquisitor",
				 "Executioner",
				 "Tormentor",
				 "Crucifier",
				 "Nyx",
				 "Aeon",
				 "Wyvern",
				 "Hel",
				 "SC",
				 "Erebus",
				 "Avatar",
				 "Ragnarok",
				 "Leviathan",
				 "Titan",
				 "Falcon",
				 "Blackbird",
				 "Scimitar",
				 "Scimi",
				 "Basi",
				 "Basilisk",
				 "Oneiros",
				 "Guardian",
				 "Armageddon",
				 "Apocalypse",
				 "Abaddon",
				 "Raven",
				 "Rokh",
				 "Scorpion",
				 "Dominix",
				 "Megathron",
				 "Hyperion",
				 "Typhoon",
				 "Tempest",
				 "Maelstrom",
				 "Drake",
				 "Hurricane",
				 "Myrmidon",
				 "Harbinger",
				 "Ferox",
				 "Cyclone",
				 "Prophecy",
				 "Brutix",
				 "Talos",
				 "Oracle",
				 "Naga",
				 "Tornado",
				 "Vindicator",
				 "Rattlesnake",
				 "Bhaalgorn",
				 "Machariel",
				 "Nightmare",
				 "Thorax",
				 "Rupture",
				 "Moa",
				 "Maller",
				 "Gate",
				 "POS",
				 "Station",
				 "Hulk",
				 "Orca",
				 "Proteus",
				 "Tengu",
				 "Legion",
				 "Loki",
				 "Velator",
				 "Goon",
				 "@the Mittani",
				 "@Shadoo",
				 "@Wrik Hoover",
				 "@Phreeze",
				 "@progodlegend",
				 "@Boodabooda",
				 "@Dysphonia",
				 "@Durrhurrdurr"]
				 
		expletives=[]
		for i in range(40):
			expletives.append("")
		
		expletives.extend(["fucking ",
						   "god damn ",
						   "bloody ",
						   "retarded ",
						   "shitty ",
						   "terribad ",])
						   
		dates=["January",
			   "Febuary",
			   "March",
			   "April",
			   "May",
			   "June",
			   "July",
			   "August",
			   "September",
			   "October",
			   "November",
			   "December"]
			
		for i in range(10):
			dates.append(str(2013+i))
				 
		t=random.choice(targets)
		e=random.choice(expletives).lower()
		if t[0]!="@":
			t=e+t
		else:
			t="@"+e+t[1:]
		c=random.choice(commands)
		if not t.startswith("@"):
			r=random.random()
			if r>0.5 and not "%|" in c:
				t_var="~"
			else:
				t_var=t
				
				
			c=c.replace("#^", "~")
				
			c=c.replace("%","the "+t_var)
			c=c.replace("#",t)
			c=c.replace("{","my "+t)
			if t.lower().startswith("a") or t.lower().startswith("e") or t.lower().startswith("i") or t.lower().startswith("o") or t.lower().startswith("u"):
				c=c.replace("$","an "+t)
			else:
				c=c.replace("$","a "+t)
			
			if "~" in c:
				if t[-2:]=="us":
					c=c.replace("~",endreplace(t,"us","ii"))
					c=c.replace("^","are")
				elif t[-1]=="x":
					c=c.replace("~",endreplace(t,"x","xen"))
					c=c.replace("^","are")
				elif t[-2:]=="as":
					c=c.replace("~",endreplace(t,"as","ae"))
					c=c.replace("^","are")
				elif t[-1]=="s":
					c=c.replace("~",t+"es")
					c=c.replace("^","are")
				else:
					c=c.replace("~",t+"s")
					c=c.replace("^","are")
			
			c=c.replace("^","is")
			
		else:
			t=t.replace("@","")
			c=c.replace("#^","#")
			c=c.replace("{",t)
			c=c.replace("%",t)
			c=c.replace("#","of "+t)
			c=c.replace("$",t)
			c=c.replace("~",t)
			c=c.replace("^","is")
		r=random.randint(1,6)*5
		c=c.replace("[]",random.choice(dates))
		c=c.replace("*",str(r))
		c=c.replace("|","")
		c=c[0].upper()+c[1:]
		
		return c