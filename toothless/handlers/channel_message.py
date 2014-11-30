import random

from ircutils import format

from toothless.decorators import command_handler
from toothless.util import humanise_list, normalise


@command_handler('attack', has_args=True)
def attack(bot, event, command, args):
    message = random.choice(bot.config.messages.attacks).format(target=args)
    formatted_message = format.color(message, format.GREEN)
    bot.send_action(bot.config.connection.channel, formatted_message)
    return True


@command_handler('eat', has_args=True)
def eat(bot, event, command, args):
    victim = args
    normalised_victim = normalise(victim)

    if normalised_victim not in bot.config.inedible_victims:
        bot.state.stomach[normalised_victim] = victim
        message = bot.config.messages.eat.format(victim=victim)
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
        bot.save_state()
    else:
        message = bot.config.messages.eat_inedible.format(victim=victim)
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
    return True


@command_handler('stomach')
def stomach(bot, event, command, args):
    stomach = bot.state.stomach.values()
    stomach.sort()
    message = bot.config.messages.stomach.format(
        victims=humanise_list(stomach)
    )
    formatted_message = format.color(message, format.GREEN)
    bot.send_action(bot.config.connection.channel, formatted_message)
    return True


@command_handler('spit', has_args=True)
def spit(bot, event, command, args):
    victim = args
    normalised_victim = normalise(victim)

    if normalised_victim in bot.state.stomach:
        del bot.state.stomach[normalised_victim]
        message = bot.config.messages.spit.format(victim=victim)
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
        bot.save_state()
    else:
        message = bot.config.messages.spit_superfluous.format(victim=victim)
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
    return True


@command_handler('vomit')
def vomit(bot, event, command, args):
    if bot.state.stomach:
        bot.state.stomach.clear()
        message = bot.config.messages.vomit
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
        bot.save_state()
    else:
        message = bot.config.messages.vomit_superfluous
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
    return True


channel_message_handlers = [
    attack,
    eat,
    stomach,
    spit,
    vomit,
]
