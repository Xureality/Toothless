from ircutils import bot, format
import random
import re
import time

__version__ = '0.2.3b "Gronckle"'  # increment this every pull/update

const_regex = r"Toothless\$\s+(.*)\s+->\s+(.*)\s*"
const_deregex = r"Toothless\#\s+(.*)"
const_eatregex = r"[T|t]oothless\!\s(.*)"
const_attregex = r"[T|t]oothless\s+attack\s+(.*[^-~`!@#$%^&*()_=+\[\]{}\\|;:\'\",.<>/?]+)"
const_treply = 0.00
const_tcommand = 0.00
err_msg = "tilts his head in confusion towards {0}"
err_msg_eat = "cocks his head in confusion at {0}'s command"


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
        global const_regex
        global const_deregex
        global err_msg
        global const_eatregex
        global const_attregex
        global err_msg_eat

        # EATING IS MORE IMPORTANT SO IT GOES ON TOP
        try:
            ms = re.match(const_eatregex, event.message)
            com = ms.group(1).split(' ', 1)  # falling back to the old way
            cmd = com[0].upper()
            if ms.group(0) and time.time() >= const_treply + 10:
                if cmd == "EAT":
                    if com[1].upper() in open('cant_eat.txt').read().upper():
                        self.send_action("#httyd", format.color(err_msg_eat.format(event.source), format.GREEN))
                    else:
                        with open('stomach.txt', "a") as f:
                            f.write(("\n%s" % (com[1])))
                            print "i just ate " + com[1]
                            msg = "gulps down " + com[1]
                            const_tcommand = time.time()
                            self.send_action("#httyd", format.color(msg.format(event.source), format.GREEN))
                elif cmd == "STOMACH":
                    f = open("stomach.txt", "r")
                    lines = f.readlines()
                    f.close()
                    message = ", ".join(''.join(s).rstrip('\n') for s in lines)
                    msg = "stomach contains " + message
                    const_tcommand = time.time()
                    self.send_action("#httyd", format.color(msg.format(event.source), format.GREEN))
                elif cmd == "SPIT":
                    f = open("stomach.txt", "r")
                    lines = f.readlines()
                    f.close()
                    f = open("stomach.txt", "w")
                    for line in lines:
                        if not re.search(com[1].upper(), line.upper()):
                            f.write(line)
                    msg = "spits out " + com[1]
                    const_tcommand = time.time()
                    self.send_action("#httyd", format.color(msg.format(event.source), format.GREEN))
                    f.close()
                elif cmd == 'SPITALL':
                    open("stomach.txt", "w").close()
                    self.send_action("#httyd", format.color("emptied his stomach", format.GREEN))

        except AttributeError:
            # print "no match"
            pass

        # ATTACKING NICKS
        try:
            attack = re.match(const_attregex, event.message)
            if attack.group(1):
                print "attack command works! Attacking %s" % attack.group(1)
                lines = open('attack_moves.txt').read().splitlines()
                line = random.choice(lines)  # '%s' possible in file lines?
                message = format.color(line + " %s" % attack.group(1), format.GREEN)
                self.send_action("#httyd", message)
        except AttributeError:
            pass

        # REMOVE COMMAND
        m = re.match(const_deregex, event.message)
        try:  # first rule of good program structure - don't follow the rules
            if m.group(0):
                if len(event.message) <= 100:
                    if event.source in open('whitelist.txt').read():
                        # print "match"
                        f = open("commands.txt", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("commands.txt", "w")
                        for line in lines:
                            if not re.search(m.group(1)+r'\s+->', line):
                                f.write(line)
                        self.send_action("#httyd", format.color("forgot one of his tricks!", format.GREEN))
                        f.close()
                    else:
                        self.send_action("#httyd", format.color("wont follow {0}'s instructions".format(event.source), format.GREEN))
                else:
                    self.send_action("#httyd", format.color(err_msg.format(event.source), format.GREEN))
        except AttributeError:
            # print "no match"
            pass

        # CHECK IF COMMAND EXISTS
        msg_split = event.message.split()
        if msg_split[0] == 'Toothless$':
            pass
            # print "missing arguments!"
        elif time.time() >= const_treply + 10:  # checks the time

            ''' # WIP
            f = open('commands.txt')
            lines = f.readlines()
            open('cmd_cache.txt', "w").close() # flush content
            with open('cmd_cache.txt', "w") as appendcmd:
                for line in lines:
                    curr_fcmd = re.match(const_regex, line)
                    if curr_fcmd.group(1).upper() in event.message.upper():
                        appendcmd.write("%s\n" % curr_fcmd.group(1))
            appendcmd.close()

            with open('cmd_cache.txt') as cache:
                for c_line in cache:

            '''

            with open('commands.txt') as f:
                for line in f:
                    f_command = re.match(const_regex, line)
                    if f_command.group(1).upper() in event.message.upper():  # for non-case-sensitivity
                        const_treply = time.time()  # updates the timer
                        if '{0}' in f_command.group(2):
                            self.send_action("#httyd", format.color(f_command.group(2).format(event.source), format.GREEN))
                        else:
                            self.send_action("#httyd", format.color(f_command.group(2), format.GREEN))
            f.close()

        # ADD COMMAND
        m = re.match(const_regex, event.message)
        try:
            if m.group(0):
                if len(event.message) <= 100:
                    if event.source in open('whitelist.txt').read() and time.time() >= const_treply + 45:  # checks the time
                        print "match"
                        with open('commands.txt', "a") as f:
                            f.write(("\nToothless$ %s -> %s" % (m.group(1), m.group(2))))
                            print "command added!"
                            const_tcommand = time.time()  # updates the timer
                            self.send_action("#httyd", format.color("has been trained by {0}!".format(event.source), format.GREEN))
                    else:
                        self.send_action("#httyd", format.color("doesn't want to be trained by {0}".format(event.source), format.GREEN))
                else:
                    self.send_action("#httyd", format.color(err_msg.format(event.source), format.GREEN))
        except AttributeError:
            # print "no match" # debug
            pass

    def on_ctcp_action(self, event):
        global const_treply
        message = " ".join(''.join(s) for s in event.params)
        if time.time() >= const_treply + 10:  # checks the time
            with open('commands.txt') as f:
                for line in f:
                    f_command = re.match(const_regex, line)
                    if f_command.group(1).upper() in message.upper():  # forces everything to ALL CAPS because reasons
                        const_treply = time.time()  # updates the timer
                        if '{0}' in f_command.group(2):
                            self.send_action("#httyd", format.color(f_command.group(2).format(event.source), format.GREEN))
                        else:
                            self.send_action("#httyd", format.color(f_command.group(2), format.GREEN))
            f.close()

    def on_private_message(self, event):
        # parse the message
        message = event.message.split()
        command = message[0].upper()  # the command is the first word
        params = message[1:]          # any wors after that are params

        # determine what to do
        if command == 'JOIN' and event.source in open('admins.txt').read():
            self.join_channel(params[0])
            message = format.color(format.bold("enters the arena!"), format.GREEN)
            self.send_action(params[0], message)
        elif command == 'TERMINATE' and event.source in open('admins.txt').read():
            self.disconnect("forced to save Hiccup from another gliding accident... again")
        elif command == 'IDENTIFY' and params and event.source in open('admins.txt').read():
            passwd = ''.join(params)
            self.send_message("NickServ", "IDENTIFY %s" % passwd)
        elif command == 'IGNORE_ME':
            with open('exclude_users.txt', "a") as appendnick:
                appendnick.write("\n%s" % event.source)
        elif command == 'APPEND_WHITELIST' and event.source in open('admins.txt').read():
            with open('whitelist.txt', "a") as appendnick:
                appendnick.write("\n%s" % params[0])
                self.send_action(event.source, "has added %s to the whitelist!" % params[0])
                appendnick.close()
        elif command == 'LIST_COMMANDS':
            f = open('commands.txt', "r")
            lines = f.readlines()
            f.close()
            for line in lines:
                m = re.match(const_regex, line)
                message = "%s -> %s" % (m.group(1), m.group(2))
                self.send_message(event.source, message)
        elif command == 'PURGE_COMMANDS_CONFIRM' and event.source in open('admins.txt').read():
            open('commands.txt', "w").close()
