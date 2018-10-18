import logging
import datetime

from discord.ext import commands


class LogCog:
    """Logs everything."""

    def __init__(self, bot):
        self.bot = bot

        self.debugLogger = logging.getLogger('discord')
        self.debugLogger.setLevel(logging.DEBUG)
        self.debugHandler = logging.FileHandler(filename = 'logs/cueball_debug.log', encoding = 'utf-8', mode = 'w')
        self.debugHandler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s ::\t%(name)s:  %(message)s'))
        self.debugLogger.addHandler(self.debugHandler)

        self.cmdLogger = logging.basicConfig(level = logging.INFO)
        self.cmdHandler = logging.FileHandler(filename = 'logs/cueball_cmd.log', encoding = 'utf-8', mode = 'w')
        self.cmdHandler.setFormatter(logging.Formatter(''))
        self.cmdLogger.addHandler(self.cmdHandler)

    @commands.command()
    async def on_command(self, ctx):
        self.cmdLogger.info(f"{datetime.datetime.now()} :: {ctx.command}")
        print(f"{datetime.datetime.now()} :: {ctx.command}")


def setup(bot):
    bot.add_cog(LogCog(bot))
