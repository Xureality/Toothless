from ircutils.events import CTCPEvent


def admin_handler(deny_handler):
    def outer(handler):
        def inner(bot, event, *args, **kwargs):
            if not (event.source in bot.config.admin_nicks):
                deny_handler(bot, event)
                return True  # Stop processing chain here.
            return handler(bot, event, *args, **kwargs)
        return inner
    return outer


def privileged_handler(deny_handler):
    def outer(handler):
        def inner(bot, event, *args, **kwargs):
            if not ((event.source in bot.config.admin_nicks) or
                    (event.source in bot.state.privileged_nicks)):
                deny_handler(bot, event)
                return True  # Stop processing chain here.
            return handler(bot, event, *args, **kwargs)
        return inner
    return outer


def command_handler(name, has_args=False):
    def outer(handler):
        def inner(bot, event, command, args):
            if not ((command == name) and (bool(args) == has_args)):
                return False  # No match; continue processing chain.
            return handler(bot, event, command, args)
        return inner
    return outer


def message_handler(handler):
    def inner(bot, event, *args, **kwargs):
        if isinstance(event, CTCPEvent):
            event.message = ' '.join(event.params)
        return handler(bot, event)
    return inner


def rate_limited_handler(rate_limiter):
    def outer(handler):
        def inner(bot, event, *args, **kwargs):
            # Enforce rate limiting on a per-nick basis.
            if rate_limiter(bot).intend(event.source)[0] < 0:
                return True  # Stop processing chain here.
            return handler(bot, event, *args, **kwargs)
        return inner
    return outer
