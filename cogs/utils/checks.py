from discord.ext import commands
from .settings import settings


def check_is_auth(ctx):
    return ctx.message.author.id in settings.auth_users


def is_auth():
    return commands.check(check_is_auth)


def check_permissions(ctx, perms):
    if check_is_auth(ctx):
        return True
    elif not perms:
        return False

    ch = ctx.message.channel
    author = ctx.message.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def has_perms():
    return commands.check(check_permissions)
