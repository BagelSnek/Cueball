import logging

from discord.ext import commands


class Logger:
    """Logs everything."""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(filename = 'cueball.log', encoding = 'utf-8', mode = 'w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s :: %(levelname)s ::\t%(name)s:  %(message)s'))
        self.logger.addHandler(self.handler)

    @commands.command()
    async def on_command(self, ctx):
        self.logger.info(ctx.command)
