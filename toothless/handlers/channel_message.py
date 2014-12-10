import random
import re

from heapq import heappush
from string import Template

from toothless.decorators import (command_handler, message_handler,
                                  privileged_handler)
from toothless.models import Command
from toothless.util import dispatch, humanise_list, normalise


LEARN_COMMAND = re.compile('(?P<trigger>.+) -> (?P<response>.+)')


@command_handler('attack', has_args=True)
def attack(bot, event, command, args):
    bot.send_channel_action(random.choice(bot.config.messages.attacks),
                            target=args)
    return True


@command_handler('eat', has_args=True)
def eat(bot, event, command, args):
    victim = args
    normalised_victim = normalise(victim)

    if normalised_victim not in bot.config.inedible_victims:
        bot.state.stomach[normalised_victim] = victim
        bot.send_channel_action(bot.config.messages.eat, victim=victim)
        bot.save_state()
    else:
        bot.send_channel_action(bot.config.messages.eat_inedible,
                                victim=victim)
    return True


@command_handler('stomach')
def stomach(bot, event, command, args):
    stomach = bot.state.stomach.values()
    stomach.sort()
    bot.send_channel_action(bot.config.messages.stomach,
                            victims=humanise_list(stomach))
    return True


@command_handler('spit', has_args=True)
def spit(bot, event, command, args):
    victim = args
    normalised_victim = normalise(victim)

    if normalised_victim in bot.state.stomach:
        del bot.state.stomach[normalised_victim]
        bot.send_channel_action(bot.config.messages.spit, victim=victim)
        bot.save_state()
    else:
        bot.send_channel_action(bot.config.messages.spit_superfluous,
                                victim=victim)
    return True


@command_handler('vomit')
def vomit(bot, event, command, args):
    if bot.state.stomach:
        bot.state.stomach.clear()
        bot.send_channel_action(bot.config.messages.vomit)
        bot.save_state()
    else:
        bot.send_channel_action(bot.config.messages.vomit_superfluous)
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

        bot.send_channel_action(bot.config.messages.learn, nick=event.source)

        bot.save_state()
    except (AssertionError, re.error):
        bot.send_channel_action(bot.config.messages.learn_error,
                                nick=event.source)
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
        bot.send_channel_action(bot.config.messages.forget)
        bot.save_state()
    else:
        bot.send_channel_action(bot.config.messages.forget_superfluous)
    return True


@message_handler
def respond(bot, event):
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

    bot.send_channel_action(matches[0][1])
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
