import os
import sys
import platform
import time
import datetime
import discord
from discord.ext import commands
import logging
from logging.handlers import RotatingFileHandler
from cogs.utils.settings import settings


class Cueball(commands.Bot):
    """
    Framework for a bot, designed to be used with cogs and not as a stand-alone.
    Will eventually be converted to use the AutoShardedBot class instead of Bot.
    """

    def __init__(self, *args, **kwargs):
        def prefix_manager(bot, message):
            """
            Manages prefix for commands in each guild.

            :param message: Message to check prefix for
            :returns: The prefix of the guild for the message given
            :rtype: str
            """
            return bot.settings.get_prefixes(message.guild.id)

        self.uptime = datetime.datetime.utcnow()
        self.settings = settings
        self.logger = set_logger()

        super().__init__(*args, activity = discord.Game(name = self.settings.current_activity),
                         command_prefix = prefix_manager, **kwargs)

    # Bot startup output
    async def on_ready(self):
        print(f"{time.ctime()} :: Booted as {self.user.name} (ID - {self.user.id})")
        print(f"Playing game: {self.settings.current_activity}\n")
        print("Connected guilds:\n" + '\n'.join([f"\tID - {guild.id} : Name - {guild.name}" for guild in self.guilds]))
        print(f"Discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})\n\n")
        self.check_guilds()

    def load_cogs(self):
        print("Loading cogs...")
        for cog in self.settings.loaded_extensions:
            print(f"\tLoading {cog}...")
            try:
                self.load_extension(f"cogs.{cog}")
                print(f"\t{cog} loaded.")
            except (discord.ClientException, ImportError) as e:
                print(f"\tFailed to load {cog} || {type(e).__name__}: {e}")
                settings.disable_extension(cog)
                print(f"\tDisabling {cog}.")
        print("Cogs loaded.\n\n")

    def check_guilds(self):
        guild_ids = [guild.id for guild in self.guilds]
        for guild_id in guild_ids:
            if guild_id not in settings.guild_ids:
                settings.add_guild(guild_id)

        for guild_id in settings.guild_ids:
            if guild_id not in guild_ids:
                # settings.remove_guild(guild_id)
                print(guild_id)


def set_logger():
    logger = logging.getLogger("cueball")
    logger.setLevel(logging.INFO)

    cue_format = logging.Formatter(
        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
        '%(message)s',
        datefmt = "[%Y-%m-%d:%H:%M]")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(cue_format)
    stdout_handler.setLevel(logging.INFO)

    fhandler = RotatingFileHandler(
        filename = 'data/logs/cueball.log', encoding = 'utf-8', mode = 'a',
        maxBytes = 10 ** 7, backupCount = 3)
    fhandler.setFormatter(cue_format)

    logger.addHandler(fhandler)
    logger.addHandler(stdout_handler)

    dpy_logger = logging.getLogger("discord")
    dpy_logger.setLevel(logging.WARNING)

    handler = logging.FileHandler(
        filename = 'data/logs/discord.log', encoding = 'utf-8', mode = 'a')
    handler.setFormatter(cue_format)
    dpy_logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    bot = Cueball()
    if bot.settings.loaded_extensions != {}:
        bot.load_cogs()
    else:
        print("Running without cogs.")

    bot.run(bot.settings.token, reconnect = True)
