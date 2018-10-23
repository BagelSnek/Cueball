import datetime
import logging


class LoggerCog:
    """Logs everything."""

    def __init__(self, bot):
        self.bot = bot

        self.debugLogger = logging.getLogger('discord')
        self.debugLogger.setLevel(logging.DEBUG)
        self.debugHandler = logging.FileHandler(filename = 'logs/cueball_debug.log', encoding = 'utf-8', mode = 'w')
        self.debugHandler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s ::\t%(name)s:  %(message)s'))
        self.debugLogger.addHandler(self.debugHandler)

        self.cmdLogger = logging.getLogger(__name__)
        self.cmdLogger.setLevel(logging.INFO)
        self.cmdHandler = logging.FileHandler(filename = 'logs/cueball_cmd.log', encoding = 'utf-8', mode = 'w')
        self.cmdHandler.setFormatter(logging.Formatter('%(asctime)s ::\t %(message)s'))
        self.cmdLogger.addHandler(self.cmdHandler)

    async def on_command(self, ctx):
        self.cmdLogger.info(f"Command :: {ctx.command})")
        print(f"{datetime.datetime.now()} :: {ctx.command}")


def setup(bot):
    bot.add_cog(LoggerCog(bot))
