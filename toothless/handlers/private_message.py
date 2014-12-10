from toothless.decorators import admin_handler, command_handler
from toothless.util import dispatch, humanise_list


@command_handler('list_commands')
def list_commands(bot, event, command, args):
    idents = bot.state.commands.keys()
    idents.sort()
    for ident in idents:
        command = bot.state.commands[ident]
        message = bot.config.messages.print_command.format(
            trigger=command.trigger, response=command.response
        )
        bot.send_message(event.source, message)


@command_handler('ignore_me')
def ignore_me(bot, event, command, args):
    if event.source not in bot.state.ignored_nicks:
        bot.state.ignored_nicks.add(event.source)
        message = bot.config.messages.ignore_me
        bot.send_action(event.source, message)
        bot.save_state()
    else:
        message = bot.config.messages.ignore_me_superfluous
        bot.send_action(event.source, message)
    return True


@command_handler('append_whitelist', has_args=True)
def append_whitelist(bot, event, command, args):
    nicks = set(args.split())
    new_nicks = nicks - bot.state.privileged_nicks
    existing_nicks = nicks & bot.state.privileged_nicks
    bot.state.privileged_nicks.update(new_nicks)

    new_nicks_sorted = list(new_nicks)
    new_nicks_sorted.sort()
    message = bot.config.messages.append_whitelist_new.format(
        nicks=humanise_list(new_nicks_sorted, zero_items='nobody')
    )
    if existing_nicks:
        message += ' ' + bot.config.messages.append_whitelist_existing
    bot.send_action(event.source, message)

    if new_nicks:
        bot.save_state()
    return True


@command_handler('purge_commands')
def purge_commands(bot, event, command, args):
    if bot.state.commands:
        bot.state.commands.clear()
        bot.commands_cache.clear()
        message = bot.config.messages.purge_commands
        bot.send_action(event.source, message)
        bot.save_state()
    else:
        message = bot.config.messages.purge_commands_superfluous
        bot.send_action(event.source, message)
    return True


@command_handler('reload_config')
def reload_config(bot, event, command, args):
    bot.load_config()
    bot.load_state()
    return True


@command_handler('terminate')
def terminate(bot, event, command, args):
    bot.disconnect(bot.config.messages.disconnect)
    return True


admin_private_message_handlers = [
    append_whitelist,
    purge_commands,
    reload_config,
    terminate,
]


private_message_handlers = [
    list_commands,
    ignore_me,
    admin_handler(
        lambda *args: dispatch(admin_private_message_handlers, *args)
    ),
]
