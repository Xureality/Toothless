import json

from ircutils.bot import SimpleBot

from toothless.handlers import (channel_message_handlers, ctcp_action_handlers,
                                join_handlers, private_message_handlers)
from toothless.models import Config, State
from toothless.util import dispatch


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

    def on_any(self, event):
        print(u'{0} ({1} \u2192 {2}) {3}'.format(event.command, event.source,
                                                 event.target, event.params))

    def on_channel_message(self, event):
        dispatch(channel_message_handlers, self, event)

    def on_ctcp_action(self, event):
        dispatch(ctcp_action_handlers, self, event)

    def on_join(self, event):
        dispatch(join_handlers, self, event)

    def on_private_message(self, event):
        dispatch(private_message_handlers, self, event)
