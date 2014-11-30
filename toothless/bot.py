import json
import logging
import os
import re

from ircutils.bot import SimpleBot
from string import Template

from toothless.handlers import (channel_message_handlers, ctcp_action_handlers,
                                join_handlers, private_message_handlers)
from toothless.models import Config, State
from toothless.util import RateLimiter, dispatch, normalise


logger = logging.getLogger(__name__)


class Bot(SimpleBot):
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

        self.channel_message_command_parser = re.compile(
            '^\s*' + self.nickname + '!\s*(?P<command>\w+)\s*(?P<args>.*)$',
            re.IGNORECASE
        )
        self.private_message_command_parser = re.compile(
            '^\s*(?P<command>\w+)\s*(?P<args>.*)$',
            re.IGNORECASE
        )

    def load_config(self):
        self.config_file.seek(0)
        self.config = Config(json.load(self.config_file))
        self.command_responses_rate_limiter = RateLimiter(
            self.config.throttle_command_responses.quota,
            self.config.throttle_command_responses.window
        )

    def load_state(self):
        try:
            self.state_file.seek(0)
            self.state = State(json.load(self.state_file))
        except:
            self.state = State()
        self.commands_cache = {
            ident: (re.compile(command.trigger), Template(command.response))
            for (ident, command) in self.state.commands.iteritems()
        }

    def save_state(self):
        self.state_file.truncate(0)
        json.dump(self.state.to_json(), self.state_file, indent=4,
                  separators=(',', ': '), sort_keys=True)
        self.state_file.flush()
        os.fsync(self.state_file.fileno())

    def on_welcome(self, event):
        if self.config.connection.password:
            self.identify(self.config.connection.password)
        self.join(self.config.connection.channel)

    def on_any(self, event):
        logger.debug(u'Received %s (%s \u2192 %s): %s', event.command,
                     event.source, event.target, event.params)

    def on_channel_message(self, event):
        if event.source != self.nickname:
            match = self.channel_message_command_parser.match(event.message)
            dispatch(channel_message_handlers, self, event,
                     normalise(match.group('command')) if match else None,
                     match.group('args').strip() if match else None)

    def on_ctcp_action(self, event):
        if event.source != self.nickname:
            dispatch(ctcp_action_handlers, self, event)

    def on_join(self, event):
        dispatch(join_handlers, self, event)

    def on_private_message(self, event):
        if event.source != self.nickname:
            match = self.private_message_command_parser.match(event.message)
            dispatch(private_message_handlers, self, event,
                     normalise(match.group('command')) if match else None,
                     match.group('args').strip() if match else None)
