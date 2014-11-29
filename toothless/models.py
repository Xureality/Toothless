from jsonobject import (BooleanProperty, DictProperty, IntegerProperty,
                        JsonObject, ListProperty, ObjectProperty, SetProperty)

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
    attacks = ListProperty(str, required=True)
    greetings = ListProperty(str, required=True)


class Config(JsonObject):
    admin_nicks = SetProperty(str, required=True)
    connection = ObjectProperty(ConnectionConfig, required=True)
    inedible_victims = SetProperty(str)
    messages = ObjectProperty(MessagesConfig, required=True)


class State(JsonObject):
    ignored_nicks = SetProperty(str)
    privileged_nicks = SetProperty(str)
    stomach = DictProperty(str)
