import random

from ircutils import format


def greet_newcomer(bot, event):
    if not ((event.source not in bot.state.ignored_nicks) and
            (event.source != bot.nickname)):
        return False

    message = random.choice(bot.config.messages.greetings).format(
        nick=event.source
    )
    formatted_message = format.color(message, format.GREEN)
    bot.send_action(bot.config.connection.channel, formatted_message)
    return True


def announce_arrival(bot, event):
    if not (event.source == bot.nickname):
        return False

    message = bot.config.messages.announce_arrival
    formatted_message = format.color(format.bold(message), format.GREEN)
    bot.send_action(bot.config.connection.channel, formatted_message)
    return True


join_handlers = [
    greet_newcomer,
    announce_arrival,
]
