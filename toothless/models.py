from jsonobject import (BooleanProperty, DictProperty, FloatProperty,
                        IntegerProperty, JsonObject, ListProperty,
                        ObjectProperty, SetProperty)

from toothless.util import AsciiStringProperty


JsonObject.Meta.properties[str] = AsciiStringProperty


class ConnectionServerConfig(JsonObject):
    address = AsciiStringProperty(required=True)
    port = IntegerProperty(required=True)
    use_ssl = BooleanProperty(default=False)


class ConnectionConfig(JsonObject):
    channel = AsciiStringProperty(required=True)
    nick = AsciiStringProperty(required=True)
    password = AsciiStringProperty()
    real_name = AsciiStringProperty()
    server = ObjectProperty(ConnectionServerConfig, required=True)
    user_name = AsciiStringProperty()


class MessagesConfig(JsonObject):
    announce_arrival = AsciiStringProperty(required=True)
    append_whitelist_existing = AsciiStringProperty(required=True)
    append_whitelist_new = AsciiStringProperty(required=True)
    attacks = ListProperty(str, required=True)
    deny = AsciiStringProperty(required=True)
    disconnect = AsciiStringProperty(required=True)
    eat = AsciiStringProperty(required=True)
    eat_inedible = AsciiStringProperty(required=True)
    forget = AsciiStringProperty(required=True)
    forget_superfluous = AsciiStringProperty(required=True)
    greetings = ListProperty(str, required=True)
    ignore_me = AsciiStringProperty(required=True)
    ignore_me_superfluous = AsciiStringProperty(required=True)
    learn = AsciiStringProperty(required=True)
    learn_deny = AsciiStringProperty(required=True)
    learn_error = AsciiStringProperty(required=True)
    print_command = AsciiStringProperty(required=True)
    purge_commands = AsciiStringProperty(required=True)
    purge_commands_superfluous = AsciiStringProperty(required=True)
    roll = AsciiStringProperty(required=True)
    nodice = AsciiStringProperty(required=True)
    spit = AsciiStringProperty(required=True)
    spit_superfluous = AsciiStringProperty(required=True)
    stomach = AsciiStringProperty(required=True)
    urltitle = AsciiStringProperty(required=True)
    vomit = AsciiStringProperty(required=True)
    vomit_superfluous = AsciiStringProperty(required=True)


class RateLimiterArgs(JsonObject):
    quota = IntegerProperty(required=True)
    window = FloatProperty(required=True)


class Config(JsonObject):
    admin_nicks = SetProperty(str, required=True)
    connection = ObjectProperty(ConnectionConfig, required=True)
    inedible_victims = SetProperty(str)
    messages = ObjectProperty(MessagesConfig, required=True)
    throttle_command_responses = ObjectProperty(RateLimiterArgs, required=True)


class Command(JsonObject):
    trigger = AsciiStringProperty(required=True)
    response = AsciiStringProperty(required=True)


class State(JsonObject):
    commands = DictProperty(Command)
    ignored_nicks = SetProperty(str)
    privileged_nicks = SetProperty(str)
    stomach = DictProperty(str)
