def admin_handler(func):
    def inner(bot, event, *args, **kwargs):
        if not (event.source in bot.config.admin_nicks):
            return False
        return func(bot, event, *args, **kwargs)
    return inner


def privileged_handler(func):
    def inner(bot, event, *args, **kwargs):
        if not ((event.source in bot.config.admin_nicks) or
                (event.source in bot.state.privileged_nicks)):
            return False
        return func(bot, event, *args, **kwargs)
    return inner


def command_handler(name, has_args=False):
    def outer(func):
        def inner(bot, event, command, args):
            if not ((command == name) and (bool(args) == has_args)):
                return False
            return func(bot, event, command, args)
        return inner
    return outer
