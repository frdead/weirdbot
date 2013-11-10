#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
	SleekXMPP: The Sleek XMPP Library
	Copyright (C) 2010  Nathanael C. Fritz
	This file is part of SleekXMPP.

	See the file LICENSE for copying permission.
"""

import sys, os, time
import logging
import getpass
import threading
from optparse import OptionParser
from lib import misc
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
	def __init__(self, jid, password, room, nick, log):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)

		self.room = room
		self.nick = nick
		global logmode
		logmode = log
		self.add_event_handler("session_start", self.start)

		self.add_event_handler("groupchat_message", self.muc_message)

		self.add_event_handler("muc::%s::got_online" % self.room,
								self.muc_online)

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
	opts, args = optp.parse_args()
	opts.jid = getc['JID']
	opts.password = getc['PASS']
	opts.room = getc['DEFAULT_ROOM']
	opts.nick = getc['NICKNAME']
	opts.log = int(getc['LOGMODE'])
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
	if opts.log is None:
		opts.log = 0

	xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick, opts.log)
	xmpp.register_plugin('xep_0030') # Service Discovery
	xmpp.register_plugin('xep_0045') # Multi-User Chat
	xmpp.register_plugin('xep_0199') # XMPP Ping

	if xmpp.connect():
		xmpp.process(block=True)
		print("Done")
	else:
		print("Unable to connect.")
