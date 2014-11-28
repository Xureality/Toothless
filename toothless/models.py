from jsonobject import (BooleanProperty, DictProperty, IntegerProperty,
                        JsonObject, ListProperty, ObjectProperty, SetProperty)

from toothless.util import AsciiStringProperty


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
    attacks = ListProperty(AsciiStringProperty, required=True)
    greetings = ListProperty(AsciiStringProperty, required=True)


class Config(JsonObject):
    admin_nicks = SetProperty(AsciiStringProperty, required=True)
    connection = ObjectProperty(ConnectionConfig, required=True)
    inedible_victims = SetProperty(AsciiStringProperty)
    messages = ObjectProperty(MessagesConfig, required=True)


class State(JsonObject):
    ignored_nicks = SetProperty(AsciiStringProperty)
    privileged_nicks = SetProperty(AsciiStringProperty)
    stomach = DictProperty(AsciiStringProperty)
