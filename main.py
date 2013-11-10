#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
	SleekXMPP: The Sleek XMPP Library
	Copyright (C) 2010  Nathanael C. Fritz
	This file is part of SleekXMPP.

	See the file LICENSE for copying permission.
"""

<<<<<<< HEAD
import sys, os, time
=======
import sys, os
>>>>>>> 9824d354d4477c517f2eb382958d668057782b85
import logging
import getpass
import threading
from optparse import OptionParser
<<<<<<< HEAD
from lib import misc
=======

>>>>>>> 9824d354d4477c517f2eb382958d668057782b85
import sleekxmpp

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
	reload(sys)
	sys.setdefaultencoding('utf8')
else:
	raw_input = input

class MUCBot(sleekxmpp.ClientXMPP):
<<<<<<< HEAD
	def __init__(self, jid, password, room, nick, log):
=======


	def __init__(self, jid, password, room, nick):
>>>>>>> 9824d354d4477c517f2eb382958d668057782b85
		sleekxmpp.ClientXMPP.__init__(self, jid, password)

		self.room = room
		self.nick = nick
<<<<<<< HEAD
		global logmode
		logmode = log
=======

>>>>>>> 9824d354d4477c517f2eb382958d668057782b85
		self.add_event_handler("session_start", self.start)

		self.add_event_handler("groupchat_message", self.muc_message)

		self.add_event_handler("muc::%s::got_online" % self.room,
<<<<<<< HEAD
								self.muc_online)
=======
							   self.muc_online)

>>>>>>> 9824d354d4477c517f2eb382958d668057782b85

	def start(self, event):
		"""
		Process the session_start event.

		Typical actions for the session_start event are
		requesting the roster and broadcasting an initial
		presence stanza.

		Arguments:
			event -- An empty dictionary. The session_start
					 event does not provide any additional
					 data.
		"""
		self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].joinMUC(self.room,
										self.nick,
										wait=True)
<<<<<<< HEAD

	def muc_message(self, msg):
		logfile = "log.txt"
		logfile2 = open(logfile, 'a')
		if logmode==1:
			if msg['body'] != "":
				logfile2.write(msg['mucnick'] + ": " + msg['body'] + "\n")
		if msg['body'].startswith("turn"): 
			if msg['body'] != "turn":
				msg.reply(msg['mucnick'] + ": " + misc.turn(msg['body'].split("turn ")[1]) % msg).send()
			else:
				lastmsgs = []
				if logmode==0:
					msg.reply(msg['mucnick'] + ": " + "Эта команда работает только со включенными логами!" % msg).send()
				else:
					for line in open(logfile):
						if line.startswith(msg['mucnick'] + ":"):
							lastmsgs.append(line)
					#msg.reply("Your last msg: " + str(lastmsgs[-2:]) % msg).send()
					msg.reply(msg['mucnick'] + ": " + misc.turn(lastmsgs[-2:][1].split(msg['mucnick'] + ":")[1].split("\n")[0]) % msg).send()
		logfile2.close()
	def muc_online(self, presence):
		pass
=======
	global weird
	#это функция из import this, впринципе запилил just for fun
	def weird(s):
		d = {}
		for c in (65, 97):
			for i in range(26):
				d[chr(i+c)] = chr((i+13) % 26 + c)
		return "".join([d.get(c, c) for c in s])
	def muc_message(self, msg):
		#вот эта фигня пишет все сообщения в консоль, прикрутил для дебага, впринципе можно в легкую логи сделать
		if msg['body'] != "": print(msg['mucnick'] + ": " + msg['body'])
		#это уже команды, питон подзабыл, на самом деле тут надо прикрутить префикс и наверное в отдельный файл вывести
		if msg['body'].startswith("!пинг"): msg.reply(msg['mucnick'] + ": " + "понг" % msg).send()
		if msg['body'].startswith("!инфо"): msg.reply(msg['mucnick'] + ": " + os.popen("uname -a").read().split("\n")[0] % msg).send()
		if msg['body'].startswith("!weird "): msg.reply(msg['mucnick'] + ": " + weird(msg['body'].split("!weird ")[1]) % msg).send()
	#это даже не знаю зачем, можно выпилить наверное
	def muc_online(self, presence):
		if presence['muc']['nick'] != self.nick:
			 pass
>>>>>>> 9824d354d4477c517f2eb382958d668057782b85

if __name__ == '__main__':
	configfile = "config.txt"
	f1 = open(configfile, 'r')
	getc = eval(f1.read())
	f1.close()

	optp = OptionParser()

	optp.add_option('-q', '--quiet', help='set logging to ERROR',
					action='store_const', dest='loglevel',
					const=logging.ERROR, default=logging.INFO)
	optp.add_option('-d', '--debug', help='set logging to DEBUG',
					action='store_const', dest='loglevel',
					const=logging.DEBUG, default=logging.INFO)
	optp.add_option('-v', '--verbose', help='set logging to COMM',
					action='store_const', dest='loglevel',
					const=5, default=logging.INFO)
<<<<<<< HEAD
=======
	#тут надо тоже это всё дело в конфиг вывести, а то не слишком удобно
	optp.add_option("-j", "--jid", dest="jid",
					help="JID to use")
	optp.add_option("-p", "--password", dest="password",
					help="password to use")
	optp.add_option("-r", "--room", dest="room",
					help="MUC room to join")
	optp.add_option("-n", "--nick", dest="nick",
					help="MUC nickname")
>>>>>>> 9824d354d4477c517f2eb382958d668057782b85
	opts, args = optp.parse_args()
	opts.jid = getc['JID']
	opts.password = getc['PASS']
	opts.room = getc['DEFAULT_ROOM']
	opts.nick = getc['NICKNAME']
<<<<<<< HEAD
	opts.log = int(getc['LOGMODE'])
=======
>>>>>>> 9824d354d4477c517f2eb382958d668057782b85
	logging.basicConfig(level=opts.loglevel,
						format='%(levelname)-8s %(message)s')
	if opts.jid is None:
		opts.jid = raw_input("Username: ")
	if opts.password is None:
		opts.password = getpass.getpass("Password: ")
	if opts.room is None:
		opts.room = raw_input("MUC room: ")
	if opts.nick is None:
		opts.nick = raw_input("MUC nickname: ")
<<<<<<< HEAD
	if opts.log is None:
		opts.log = 0

	xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick, opts.log)
=======

	xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick)
>>>>>>> 9824d354d4477c517f2eb382958d668057782b85
	xmpp.register_plugin('xep_0030') # Service Discovery
	xmpp.register_plugin('xep_0045') # Multi-User Chat
	xmpp.register_plugin('xep_0199') # XMPP Ping

	if xmpp.connect():
		xmpp.process(block=True)
		print("Done")
	else:
		print("Unable to connect.")
