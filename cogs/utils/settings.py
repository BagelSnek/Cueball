import platform

from .dataIO import dataIO
from copy import deepcopy
import discord
from os import listdir


class Settings:

    def __init__(self):
        if not dataIO.is_valid_json("botSettings.json"):
            self.bot_settings = {"currActivity": "",
                                 "extensions": {},
                                 "auth_users": []}
            self.save_bot_settings()
        else:
            self.bot_settings = dataIO.load_json("botSettings.json")

        if not dataIO.is_valid_json("guildData.json"):
            self.guild_data = {"default": {"prefixes": ["??"]}}
            self.save_guild_data()
        else:
            self.guild_data = dataIO.load_json("guildData.json")

        self.check_extensions()

    def save_bot_settings(self):
        """Saves self.bot_settings to a json in the data folder."""
        dataIO.dump_json("botSettings.json", self.bot_settings)

    def save_guild_data(self):
        """Saves self.guild_data to a json in the data folder."""
        dataIO.dump_json("guildData.json", self.guild_data)

    def check_extensions(self):
        extensions = list(filter(None, [file[:-3] if file[-3:] == '.py' and '__init__' not in file
                                        else None for file in listdir('cogs')]))

        for extension in extensions:
            if extension not in self.extensions:
                self.bot_settings['extensions'][extension] = {'load': False}

        for extension in self.extensions:
            if extension not in extensions:
                self.bot_settings['extensions'].__delitem__(extension)

        self.save_bot_settings()

    def disable_extension(self, extension):
        self.bot_settings['extensions'][extension]['load'] = False
        self.save_bot_settings()

    def enable_extension(self, extension):
        self.bot_settings['extensions'][extension]['load'] = True
        self.save_bot_settings()

    @property
    def current_activity(self):
        return self.bot_settings['currActivity']

    @property
    def token(self):
        with open('token.txt', 'r') as tokentxt:
            token = tokentxt.read()

        if "win" not in str(platform.platform()).lower():
            token = token[:-1]

        return token

    @property
    def auth_users(self):
        return self.bot_settings['auth_users'].copy()

    @property
    def extensions(self):
        """
        Copy of all extensions for the bot.

        :return: the bot's extensions
        :rtype: dict
        """
        return deepcopy(self.bot_settings['extensions'])

    @property
    def loaded_extensions(self):
        ret = {}
        for extension in self.extensions:
            if self.extensions[extension]['load']:
                ret[extension] = self.extensions[extension]
        return ret

    @property
    def unloaded_extensions(self):
        ret = {}
        for extension in self.extensions:
            if not self.extensions[extension]['load']:
                ret[extension] = self.extensions[extension]
        return ret

    @property
    def guilds(self):
        return deepcopy(self.guild_data)

    @property
    def guild_ids(self):
        guilds = list(filter(lambda x: x.isdigit(), self.guilds.keys()))
        return [int(guild_id) for guild_id in guilds]

    def get_guild(self, guild):
        """
        Returns copy of the guild's data from a Guild or its id.

        :param guild: The guild to be searched for in the guild settings
        :return: deep copy of the requested guild's data
        :rtype: dict
        """
        if isinstance(guild, discord.Guild):
            guild = guild.id

        if str(guild) not in self.guild_ids:
            return deepcopy(self.guilds['default'])
        return deepcopy(self.guilds[str(guild)])

    def get_prefixes(self, guild):
        """:rtype: list"""
        return self.get_guild(guild)['prefixes']

    def set_guild_prefixes(self, guild, prefixes):
        if guild is None:
            return

        if isinstance(guild, discord.Guild):
            guild = guild.id

        if guild not in self.guild_ids:
            self.add_guild(guild)
        self.guild_data[guild]['prefixes'] = prefixes
        self.save_guild_data()

    def add_guild_prefixes(self, guild, prefixes):
        self.set_guild_prefixes(guild, self.get_prefixes(guild).extend(prefixes))

    def add_guild(self, guild_id):
        self.guild_data[str(guild_id)] = deepcopy(self.guild_data['default'])
        self.save_guild_data()

    def remove_guild(self, guild_id):
        self.guild_data.__delitem__(str(guild_id))
        self.save_guild_data()


settings = Settings()
