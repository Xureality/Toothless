import json
import random
import re
import time

from ircutils import bot, format

from toothless.models import Config, State
from toothless.util import humanise_list, normalise


const_regex = r"Toothless\$\s+(.*)\s+->\s+(.*)\s*"
const_deregex = r"Toothless\#\s+(.*)"
const_eatregex = r"[T|t]oothless\!\s(.*)"
const_attregex = r"[T|t]oothless\s+attack\s+(.*[^-~`!@#$%^&*()_=+\[\]{}\\|;:\'\",.<>/?]+)"
const_treply = 0.00
const_tcommand = 0.00
err_msg = "tilts his head in confusion towards {0}"
err_msg_eat = "cocks his head in confusion at {0}'s command"


class Bot(bot.SimpleBot):
    IGNORE_EVENTS = set(('CONN_CONNECT', 'CTCP_VERSION', 'KICK',
                         'MODE', 'NICK', 'PART', 'PING', 'PRIVMSG', 'QUIT',
                         'RPL_BOUNCE', 'RPL_CREATED', 'RPL_ENDOFMOTD',
                         'RPL_ENDOFNAMES', 'RPL_GLOBALUSERS', 'RPL_LOCALUSERS',
                         'RPL_LUSERCHANNELS', 'RPL_LUSERCLIENT', 'RPL_LUSERME',
                         'RPL_LUSEROP', 'RPL_LUSERUNKNOWN', 'RPL_MOTD',
                         'RPL_MOTDSTART', 'RPL_MYINFO', 'RPL_NAMREPLY',
                         'RPL_STATSCONN', 'RPL_TOPIC', 'RPL_TOPICWHOTIME',
                         'RPL_YOURHOST', 'RPL_YOURID', 'RPL_WELCOME', 'TOPIC'))

    def __init__(self, config_file, state_file):
        self.config_file = config_file
        self.state_file = state_file
        self.load_config()
        self.load_state()

        super(Bot, self).__init__(self.config.connection.nick)
        if self.config.connection.user_name:
            self.user = self.config.connection.user_name
        if self.config.connection.real_name:
            self.real_name = self.config.connection.real_name
        self.connect(
            self.config.connection.server.address,
            port=self.config.connection.server.port,
            use_ssl=self.config.connection.server.use_ssl
        )

    def load_config(self):
        self.config_file.seek(0)
        self.config = Config(json.load(self.config_file))

    def load_state(self):
        self.state_file.seek(0)
        self.state = State(json.load(self.state_file))

    def save_state(self):
        self.state_file.truncate(0)
        json.dump(self.state.to_json(), self.state_file, indent=4,
                  separators=(',', ': '), sort_keys=True)

    def on_welcome(self, event):
        if self.config.connection.password:
            self.identify(self.config.connection.password)
        self.join(self.config.connection.channel)

    def on_join(self, event):
        if event.source == self.nickname:
            message = format.color(format.bold("enters the arena!"), format.GREEN)
            self.send_action(self.config.connection.channel, message)
        elif event.source not in self.state.ignored_nicks:
            cline = random.choice(self.config.messages.greetings)
            message = format.color(cline.format(nick=event.source), format.GREEN)
            self.send_action(self.config.connection.channel, message)

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
                if cmd == "STOMACH":
                    # TODO: Use a third-party humanisation library.
                    stomach = self.state.stomach.values()
                    stomach.sort()
                    msg = 'stomach contains ' + humanise_list(stomach)
                    const_tcommand = time.time()
                    self.send_action(self.config.connection.channel, format.color(msg.format(event.source), format.GREEN))
                elif cmd == 'SPITALL':
                    # TODO: Consider responding differently if stomach was already empty.
                    self.state.stomach.clear()
                    self.save_state()
                    self.send_action(self.config.connection.channel, format.color("emptied his stomach", format.GREEN))
                else:
                    victim = com[1].strip()
                    norm_victim = normalise(victim)
                    if cmd == "EAT":
                        if norm_victim in self.config.inedible_victims:
                            self.send_action(self.config.connection.channel, format.color(err_msg_eat.format(event.source), format.GREEN))
                        else:
                            # TODO: Consider responding differently if victim has already been consumed.
                            self.state.stomach[norm_victim] = victim
                            self.save_state()
                            print('I just ate ' + victim)
                            msg = 'gulps down ' + victim
                            const_tcommand = time.time()
                            self.send_action(self.config.connection.channel, format.color(msg.format(event.source), format.GREEN))
                    elif cmd == "SPIT":
                        # TODO: Consider responding differently if victim had not been consumed.
                        if norm_victim in self.state.stomach:
                            del self.state.stomach[norm_victim]
                            self.save_state()
                        msg = "spits out " + victim
                        const_tcommand = time.time()
                        self.send_action(self.config.connection.channel, format.color(msg.format(event.source), format.GREEN))
                        f.close()

        except AttributeError:
            # print "no match"
            pass

        # ATTACKING NICKS
        try:
            attack = re.match(const_attregex, event.message)
            if attack.group(1):
                print "attack command works! Attacking %s" % attack.group(1)
                line = random.choice(self.config.messages.attacks)
                message = format.color(line + " %s" % attack.group(1), format.GREEN)
                self.send_action(self.config.connection.channel, message)
        except AttributeError:
            pass

        # REMOVE COMMAND
        m = re.match(const_deregex, event.message)
        try:  # first rule of good program structure - don't follow the rules
            if m.group(0):
                if len(event.message) <= 100:
                    if event.source in self.state.privileged_nicks:
                        # print "match"
                        f = open("commands.txt", "r")
                        lines = f.readlines()
                        f.close()
                        f = open("commands.txt", "w")
                        for line in lines:
                            if not re.search(m.group(1)+r'\s+->', line):
                                f.write(line)
                        self.send_action(self.config.connection.channel, format.color("forgot one of his tricks!", format.GREEN))
                        f.close()
                    else:
                        self.send_action(self.config.connection.channel, format.color("wont follow {0}'s instructions".format(event.source), format.GREEN))
                else:
                    self.send_action(self.config.connection.channel, format.color(err_msg.format(event.source), format.GREEN))
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
                            self.send_action(self.config.connection.channel, format.color(f_command.group(2).format(event.source), format.GREEN))
                        else:
                            self.send_action(self.config.connection.channel, format.color(f_command.group(2), format.GREEN))
            f.close()

        # ADD COMMAND
        m = re.match(const_regex, event.message)
        try:
            if m.group(0):
                if len(event.message) <= 100:
                    if event.source in self.state.privileged_nicks and time.time() >= const_treply + 45:  # checks the time
                        print "match"
                        with open('commands.txt', "a") as f:
                            f.write(("\nToothless$ %s -> %s" % (m.group(1), m.group(2))))
                            print "command added!"
                            const_tcommand = time.time()  # updates the timer
                            self.send_action(self.config.connection.channel, format.color("has been trained by {0}!".format(event.source), format.GREEN))
                    else:
                        self.send_action(self.config.connection.channel, format.color("doesn't want to be trained by {0}".format(event.source), format.GREEN))
                else:
                    self.send_action(self.config.connection.channel, format.color(err_msg.format(event.source), format.GREEN))
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
                            self.send_action(self.config.connection.channel, format.color(f_command.group(2).format(event.source), format.GREEN))
                        else:
                            self.send_action(self.config.connection.channel, format.color(f_command.group(2), format.GREEN))
            f.close()

    def on_private_message(self, event):
        # parse the message
        message = event.message.split()
        command = message[0].upper()  # the command is the first word
        params = message[1:]          # any wors after that are params

        # determine what to do
        if command == 'LIST_COMMANDS':
            f = open('commands.txt', "r")
            lines = f.readlines()
            f.close()
            for line in lines:
                m = re.match(const_regex, line)
                message = "%s -> %s" % (m.group(1), m.group(2))
                self.send_message(event.source, message)
        elif command == 'IGNORE_ME':
            self.state.ignored_nicks.add(event.source)
            self.save_state()
        elif event.source in self.config.admin_nicks:
            if command == 'TERMINATE':
                self.disconnect("Gotta go save Hiccup from another gliding accident again...")
            elif command == 'APPEND_WHITELIST':
                nick = params[0]
                # TODO: Consider responding differently if nick was already whitelisted.
                self.state.privileged_nicks.add(nick)
                self.save_state()
                self.send_action(event.source, "has added %s to the whitelist!" % nick)
            elif command == 'PURGE_COMMANDS_CONFIRM':
                open('commands.txt', "w").close()
