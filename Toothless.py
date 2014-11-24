#!/usr/bin/env python
from ircutils import bot, format
import random, re, time

const_regex = r"Toothless\$\s+(.*)\s+->\s+(.*)\s*"
const_treply=0.00
const_tcommand=0.00

def SaveCommand(left, right):
	print("saving command...")
	with open('commands.txt', "a").read() as commandlist:
		commandlist.write(("\nToothless$ %s -> %s\n" % (left, right)))

class ToothlessBot(bot.SimpleBot):
	IGNORE_EVENTS = set(('CONN_CONNECT', 'CTCP_VERSION', 'KICK',
                         'MODE', 'NICK', 'PART', 'PING', 'PRIVMSG', 'QUIT',
                         'RPL_BOUNCE', 'RPL_CREATED', 'RPL_ENDOFMOTD',
                         'RPL_ENDOFNAMES', 'RPL_GLOBALUSERS', 'RPL_LOCALUSERS',
                         'RPL_LUSERCHANNELS', 'RPL_LUSERCLIENT', 'RPL_LUSERME',
                         'RPL_LUSEROP', 'RPL_LUSERUNKNOWN', 'RPL_MOTD',
                         'RPL_MOTDSTART', 'RPL_MYINFO', 'RPL_NAMREPLY',
                         'RPL_STATSCONN', 'RPL_TOPIC', 'RPL_TOPICWHOTIME',
                         'RPL_YOURHOST', 'RPL_YOURID', 'RPL_WELCOME', 'TOPIC'))
	
	def on_join(self, event):
		if event.source in open('exclude_users.txt').read():
			return

		elif event.source != self.nickname:
			lines = open('welcomemsgs.txt').read().splitlines()
			cline = random.choice(lines)
			message = format.color(cline.format(event.source), format.GREEN)
			self.send_action("#httyd", message)

	def on_any(self, event):
		if event.command in self.IGNORE_EVENTS:
			return
		
		print('\t%s (%s->%s) %s' % (event.command,
                                    event.source, event.target,
                                    event.params))

	def on_channel_message(self, event):
		global const_treply
		global const_tcommand
		err_msg = "tilts his head in confusion towards {0}"

		msg_split = event.message.split()
		if msg_split[0] == 'Toothless$':
			print "missing arguments!"
		elif time.time() >= const_treply + 10:	#checks the time
			with open('commands.txt') as f:
				for line in f:
					f_command = re.match(const_regex, line)
					if f_command.group(1) in event.message:
						print "found the following from your command: %s!" % f_command.group(2)
						const_treply = time.time()	#updates the timer
						if '{0}' in f_command.group(2):
							self.send_action("#httyd", format.color(f_command.group(2).format(event.source), format.GREEN))
						else:
							self.send_action("#httyd", format.color(f_command.group(2), format.GREEN))
			f.close()

		m = re.match(const_regex, event.message)
		try:
			if m.group(0):
				if len(event.message) <= 100:
					if event.source in open('whitelist.txt').read() and time.time() >= const_treply + 45:	#checks the time
						print "match"
						with open('commands.txt', "a") as f:
							f.write(("Toothless$ %s -> %s\n" % (m.group(1), m.group(2))))
							print "command added!"
							const_tcommand = time.time()	#updates the timer
							self.send_action("#httyd", format.color("has been trained by {0}!".format(event.source), format.GREEN))
					else:
						self.send_action("#httyd", format.color("doesn't want to be trained by {0}".format(event.source), format.GREEN))
				else:
					self.send_action("#httyd", format.color(err_msg.format(event.source), format.GREEN))
		except AttributeError:
			print "no match"

	def on_private_message(self, event):
		# parse the message
		message = event.message.split()
		command = message[0].upper()	# the command is the first word
		params = message[1:]			# any wors after that are params

		# determine what to do
		if command == 'JOIN' and event.source in open('admins.txt').read():
			self.join_channel(params[0])
			message = format.color(format.bold("enters the arena!"), format.GREEN)
			self.send_action(params[0], message)
		elif command == 'TERMINATE' and event.source in open('admins.txt').read():
			self.disconnect("I was promised a bag of fish")
		elif command == 'IDENTIFY' and event.source in open('admins.txt').read():
			self.send_message("NickServ", "IDENTIFY XXX")
		elif command == 'IGNORE_ME':
			with open('exclude_users.txt', "a") as appendnick:
				appendnick.write("\n%s" % event.source)
		elif command == 'APPEND_WHITELIST' and event.source in open('admins.txt').read():
			with open('whitelist.txt', "a") as appendnick:
				appendnick.write("\n%s" % params[0])
				self.send_action(event.source, "has added %s to the whitelist!" % params[0])


if __name__ == "__main__":
    echo = ToothlessBot("Toothless")
    echo.user = "Toothless"
    echo.real_name = "ToothlessBot, by Tomako"
    echo.connect("irc.editingarchive.com", port=6697, use_ssl=True)
    echo.start()
