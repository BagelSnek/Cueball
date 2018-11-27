#! /usr/bin/env python3.6

import os
import platform
import time
import discord
from utils import utils
from discord.ext import commands


class Cueball(commands.Bot):
    def __init__(self):
        self.settings = utils.load_json('botSettings.json')

        # Make update command to check values in botSettings.json later.
        if self.settings is None:
            self.settings = {"prefix": "??", "currActivity": "", "initial_extensions": [], "auth_users": []}

        super().__init__(command_prefix = self.settings['prefix'], case_insensitive = True,
                         activity = discord.Game(name = self.settings['currActivity']))

    def check_authorized(self, ctx):
        return str(ctx.message.author.id) in self.settings['auth_users']

    def update_botsettings(self, key, value):
        self.settings[key] = value
        utils.dump_json('botSettings.json', self.settings)

    # Bot startup output
    async def on_ready(self):
        print(f"{time.ctime()} :: Booted as {self.user.name} (ID - {self.user.id})")
        print(f"Playing game: {self.settings['currActivity']}\n")
        print("Connected guilds:\n" + '\n'.join([f"\tID - {guild.id} : Name - {guild.name}" for guild in self.guilds]))
        print(f"Discord.py API version\t: {discord.__version__}")
        print(f"Python version\t\t\t: {platform.python_version()}")
        print(f"Running on\t\t\t\t: {platform.system()} {platform.release()} ({os.name})\n\n")

    async def on_command_error(self, context, exception):
        """Simple error handler."""
        print(f"{type(exception).__name__}: {exception}")
        if isinstance(exception, commands.MissingPermissions):
            return await context.send(embed = discord.Embed(title = "Permission Error", color = 0xFF0000,
                                                            description = "You do not have permission to"
                                                                          f" use `{self.command_prefix}{context.command.name}`!"))
        if isinstance(exception, commands.MissingRequiredArgument):
            return await context.send(embed = discord.Embed(title = "Missing Required Argument", color = 0xFF0000,
                                                            description = f"`{self.command_prefix}{context.command.name}` "
                                                                          "lacks a necessary argument"))
        elif isinstance(exception, commands.CommandNotFound):
            pass
        elif isinstance(exception.original, discord.Forbidden):
            return await context.send(embed = discord.Embed(title = "Bot Missing Permission", color = 0xFF0000,
                                                            description = "I lack the permission to execute "
                                                                          f"{self.command_prefix}{context.command.name}"))
        else:
            return await context.send(embed = discord.Embed(title = "Error",
                                                            value = f"{type(exception).__name__}: {exception}"))

    # Default Cueball commands
    @commands.command(aliases = ['remove', 'delete'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int):
        """Bulk-deletes messages from the channel."""
        await ctx.message.channel.delete_messages(await ctx.channel.history(limit = amount).flatten())

    @commands.command(name = "changeGame", aliases = ["gameChange", "changePlaying", "changeActivity"])
    @commands.check(check_authorized)
    async def change_game(self, ctx, *game):
        """Changes what the bot is playing."""
        game = ' '.join(game)
        self.update_botsettings('currActivity', game)
        await self.change_presence(activity = discord.Game(name = game))
        await ctx.send(embed = discord.Embed(title = "Command: changeActivity", color = 0x0000FF,
                                             description = f"Game was changed to {game}"))

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot and gets a response time."""
        embed = discord.Embed(title = "Command: ping", color = 0x0000FF)
        try:
            embed.description = str(round(self.latency * 100, 4)) + "ms"
            await ctx.send(embed = embed)
        except:
            await ctx.send("How did you mess up the ping command? Just tell Xaereus.")

    @commands.command()
    @commands.check(check_authorized)
    async def load(self, ctx, extension_name: str):
        """Loads an extension."""
        try:
            self.load_extension(extension_name)
            await ctx.send(f"Loaded extension: `{extension_name}`")
        except (discord.ClientException, ImportError) as exc:
            await ctx.send(f"Failed to load extension {extension_name}\n{type(exc).__name__}: {exc}")

    @commands.command()
    @commands.check(check_authorized)
    async def unload(self, ctx, extension_name: str):
        """Unloads an extension."""
        try:
            self.unload_extension(extension_name)
            await ctx.send(f"Unloaded extension: `{extension_name}`")
        except (discord.ClientException, ImportError) as exc:
            await ctx.send(f"Failed to unload extension {extension_name}\n{type(exc).__name__}: {exc}")

    @commands.command()
    async def about(self, ctx):
        """Displays basic information about the bot."""
        embed = discord.Embed(title = "Command: about", color = 0x0000FF)
        embed.add_field(name = "Name", value = self.user.name)
        embed.add_field(name = "Built by", value = "Machoo and Xaereus")
        embed.add_field(name = "Running on", value = str(platform.platform()))
        embed.add_field(name = "Github", value = "https://github.com/BagelSnek/Cueball")
        embed.add_field(name = "Servers", inline = False,
                        value = "\n".join([f"`ID - {guild.id} : Name - {guild.name}`" for guild in self.guilds]))
        if len(self.settings['initial_extensions']) > 0:
            embed.add_field(name = "Extensions", value = '\n'.join(f"`{x[x.rindex('.') + 1:]}`"
                                                                   for x in self.settings['initial_extensions']))
        await ctx.send(embed = embed)


if __name__ == '__main__':
    bot = Cueball()
    for extension in bot.settings['initial_extensions']:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension `{extension}`")
        except (AttributeError, ImportError) as e:
            print(f"Failed to load extension `{extension}`\n{type(e).__name__}: {e}")
    print("Cogs loaded.\n\n")

    with open('token.txt', 'r') as tokentxt:
        token = tokentxt.read()
    tokentxt.close()

    if "win" not in str(platform.platform()).lower():
        token = token[:-1]

    bot.run(token, reconnect = True)
