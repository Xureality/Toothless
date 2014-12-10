import random

from ircutils import format


def greet_newcomer(bot, event):
    if not ((event.source not in bot.state.ignored_nicks) and
            (event.source != bot.nickname)):
        return False

    bot.send_channel_action(random.choice(bot.config.messages.greetings),
                            nick=event.source)
    return True


def announce_arrival(bot, event):
    if not (event.source == bot.nickname):
        return False

    bot.send_channel_action(format.bold(bot.config.messages.announce_arrival))
    return True


join_handlers = [
    greet_newcomer,
    announce_arrival,
]
