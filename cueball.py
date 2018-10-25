#! /usr/bin/env python3.6

import os
import platform
import time
import json
import discord
from discord.ext.commands import Bot
from discord.ext import commands

# Load bot settings
if not os.path.isfile('botSettings.json'):
    # Creates file with default settings
    bot_settings = {"prefix": "??", "currActivity": "", "initial_extensions": [], "auth_users": []}
    json.dump(bot_settings, open('botSettings.json', 'w'), indent = 4)
else:
    with open('botSettings.json') as botSettings:
        bot_settings = json.load(botSettings)
    botSettings.close()
    print("Settings successfully loaded.")

bot = Bot(description = "Cueball shall rule.", command_prefix = bot_settings['prefix'], case_insensitive = True,
          activity = discord.Game(name = bot_settings['currGame']))


def check_authorized():
    def predicate(ctx):
        return str(ctx.message.author.id) in bot_settings['auth_users']
    return commands.check(predicate)


def update_botsettings(key, value):
    bot_settings[key] = value
    json.dump(bot_settings, open('botSettings.json', 'w'), indent = 4)
    return value


# Start bot and print status to console
@bot.event
async def on_ready():
    """Where we droppin', boys?"""
    print(f"{time.ctime()} :: Booted as {bot.user.name} (ID - {bot.user.id})\n")
    print("Connected guilds:")
    for guild in bot.guilds:
        print(f"\tID - {guild.id} : Name - {guild.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")


@bot.listen('check_authorized')
async def spook(ctx):
    if not check_authorized():
        await ctx.send(embed = discord.Embed(title = "Permission Error", color = 0xFF0000,
                                             description = "You do not have permission to"
                                                           f" use `{bot.command_prefix}{ctx.command.name}`!"))


# Default Cueball commands
@bot.command(aliases = ['remove', 'delete'])
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount: int):
    """Bulk-deletes messages from the channel."""
    await ctx.channel.delete([x for x in ctx.logs_from(ctx.message.channel, limit = amount)])


@bot.command(name = "listRoles", aliases = ["roles"])
async def list_roles(ctx):
    """Lists the current roles on the guild."""
    await ctx.send(embed = discord.Embed(title = "Command: listRoles", color = 0x0000FF,
                                         description = '\n'.join([f"`{role.name}`" for role in ctx.message.guild.roles])))


@bot.command(aliases = ['say'])
async def echo(ctx, *say):
    """Makes the bot talk."""
    try:
        await ctx.message.delete()
        await ctx.send(' '.join(say))
    except:
        await ctx.send("If you managed to break this command, you are a fucking wizard or a hacker.")


@bot.command(name = "changeGame", aliases = ["gameChange", "changePlaying"])
@check_authorized()
async def change_game(ctx, *game):
    """Changes what the bot is playing."""
    await bot.change_presence(game =
                              discord.Game(name = update_botsettings('currGame', ' '.join(game))))
    await ctx.send(embed = discord.Embed(title = "Command: changeGame", color = 0x0000FF,
                                         description = f"Game was changed to {' '.join(game)}"))


@bot.command(name = "getBans", aliases = ["listBans", "bans"])
async def get_bans(ctx):
    """Lists all banned users on the current guild."""
    await ctx.send(embed = discord.Embed(title = "Command: getBans", color = 0x00FF00,
                                         description =
                                         '\n'.join([y.name for y in await ctx.get_bans(ctx.message.guild)])))


@bot.command(aliases = ['user', 'whois'])
async def info(ctx, user: discord.Member):
    """Gets info on a member, such as their ID."""
    embed = discord.Embed(title = "Command: info", color = 0x0000FF)
    try:
        embed.description = user.name
        embed.add_field(name = "ID", value = user.id)
        embed.add_field(name = "Joined at", value = user.joined_at)
        embed.add_field(name = "Roles", inline = False,
                        value = "\n".join(filter(None, [role.name if role.name != "@everyone" else None
                                                        for role in user.roles])))
    except:
        embed.color = 0xFF0000
        embed.description = "How did you fuck up this command?"
    await ctx.send(embed = embed)


@bot.command()
async def ping(ctx):
    """Pings the bot and gets a response time."""
    embed = discord.Embed(title = "Command: ping", color = 0x0000FF)
    try:
        embed.description = str(round(bot.latency * 100, 4)) + "ms"
        await ctx.send(embed = embed)
    except:
        await ctx.send("How did you mess up the ping command? Just tell Xaereus.")


@bot.command()
@check_authorized()
async def load(ctx, extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
        await ctx.send(f"Loaded extension: `{extension_name}`")
    except (discord.ClientException, ImportError) as exc:
        await ctx.send(f"Failed to load extension {extension_name}\n{type(exc).__name__}: {exc}")


@bot.command()
@check_authorized()
async def unload(ctx, extension_name: str):
    """Unloads an extension."""
    try:
        bot.unload_extension(extension_name)
        await ctx.send(f"Unloaded extension: `{extension_name}`")
    except (discord.ClientException, ImportError) as exc:
        await ctx.send(f"Failed to unload extension {extension_name}\n{type(exc).__name__}: {exc}")


@bot.command()
async def about(ctx):
    """Displays basic information about the bot."""
    embed = discord.Embed(title = "Command: about", color = 0x0000FF)
    embed.add_field(name = "Name", value = bot.user.name)
    embed.add_field(name = "Built by", value = "Machoo and Xaereus")
    embed.add_field(name = "Running on", value = str(platform.platform()))
    embed.add_field(name = "Github", value = "https://github.com/BagelSnek/Cueball")
    embed.add_field(name = "Servers", inline = False,
                    value = "\n".join([f"`ID - {guild.id} : Name - {guild.name}`" for guild in bot.guilds]))
    if len(bot_settings['initial_extensions']) > 0:
        embed.add_field(name = "Extensions", value = '\n'.join(f"`{x[x.rindex('.') + 1:]}`"
                                                               for x in bot_settings['initial_extensions']))
    await ctx.send(embed = embed)


if __name__ == '__main__':
    for extension in bot_settings['initial_extensions']:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension `{extension}`")
        except (AttributeError, ImportError) as e:
            print(f'Failed to load extension `{extension}`\n{type(e).__name__}: {e}')
    with open('token.txt', 'r') as tokentxt:
        token = tokentxt.read()
    print(token)
    bot.run(token, reconnect = True)
