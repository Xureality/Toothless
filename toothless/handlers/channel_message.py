import random
import re

from heapq import heappush
from ircutils import format
from string import Template

from toothless.decorators import command_handler, privileged_handler
from toothless.models import Command
from toothless.util import dispatch, humanise_list, normalise


LEARN_COMMAND = re.compile('(?P<trigger>.+) -> (?P<response>.+)')


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


@command_handler('learn', has_args=True)
def learn(bot, event, command, args):
    trigger = args
    ident = normalise(trigger)

    try:
        # Parse instructions.
        match = LEARN_COMMAND.match(args)
        assert(match)

        # Ensure trigger is reasonably unique.
        trigger = match.group('trigger')
        response = match.group('response')
        ident = normalise(trigger)
        assert(ident not in bot.state.commands)

        # Ensure both trigger and response are valid.
        regex = re.compile(trigger)
        template = Template(response)

        # TODO: Ensure all exceptions henceforth are fatal.
        bot.state.commands[ident] = Command(trigger=trigger, response=response)
        bot.commands_cache[ident] = (regex, template)

        message = bot.config.messages.learn.format(nick=event.source)
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)

        bot.save_state()
    except (AssertionError, re.error):
        message = bot.config.messages.learn_error.format(nick=event.source)
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
    return True


@command_handler('forget', has_args=True)
def forget(bot, event, command, args):
    trigger = args
    ident = normalise(trigger)
    command_exists = ((ident in bot.state.commands) and
                      (trigger == bot.state.commands[ident].trigger))

    if command_exists:
        del bot.state.commands[ident]
        del bot.commands_cache[ident]
        message = bot.config.messages.forget
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
        bot.save_state()
    else:
        message = bot.config.messages.forget_superfluous
        formatted_message = format.color(message, format.GREEN)
        bot.send_action(bot.config.connection.channel, formatted_message)
    return True


@command_handler(None)
def respond(bot, event, command, args):
    # Enforce rate limiting on a per-nick basis.
    if bot.command_responses_rate_limiter.intend(event.source)[0] < 0:
        return False

    matches = []
    for (ident, (regex, template)) in bot.commands_cache.iteritems():
        match = regex.search(event.message)
        if match:
            params = match.groupdict()
            params['nick'] = event.source
            heappush(
                matches, (match.start(0), template.safe_substitute(params))
            )

    if not matches:
        return False

    message = matches[0][1]
    formatted_message = format.color(message, format.GREEN)
    bot.send_action(bot.config.connection.channel, formatted_message)
    return True


privileged_channel_message_handlers = [
    learn,
    forget,
]


channel_message_handlers = [
    attack,
    eat,
    stomach,
    spit,
    vomit,
    privileged_handler(
        lambda *args: dispatch(privileged_channel_message_handlers, *args)
    ),
    respond,
]
