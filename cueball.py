#! /usr/bin/env

import os
import platform
import time
import json
import discord
import requests
from discord.ext.commands import Bot

# Load bot settings
if not os.path.isfile('botSettings.json'):
    # Creates file with default settings
    bot_settings = {"prefix": "??", "currActivity": "", "initial_extensions": []}
    json.dump(bot_settings, open('botSettings.json', 'w'), indent = 4)
else:
    with open('botSettings.json') as botSettings:
        bot_settings = json.load(botSettings)
    botSettings.close()
    print("Settings successfully loaded.")

bot = Bot(description = "Cueball shall rule.", command_prefix = bot_settings['prefix'],
          activity = discord.Game(name = bot_settings['currActivity']),
          case_insensitive = True, )


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


# Default Cueball commands
@bot.command(aliases = ['remove', 'delete'])
async def purge(ctx, number: int):
    """Bulk-deletes messages from the channel."""
    if ctx.message.author.guild_permissions.administrator:
        return await ctx.delete_messages([x for x in ctx.logs_from(ctx.message.channel, limit = number)])
    await ctx.send(embed = discord.Embed(title = "Command: purge", color = 0xFF0000,
                                         description = "Ya done messed up, bother Xaereus about it."))


@bot.command(name = "listRoles", aliases = ["roles"])
async def list_roles(ctx):
    """Lists the current roles on the guild."""
    await ctx.send(embed = discord.Embed(title = "Command: listRoles", color = 0x0000FF,
                                         value = '\n'.join([role.name for role in ctx.message.guild.roles])))


@bot.command()
async def hug(ctx, *, member: discord.Member = None):
    """Hug someone on the server <3"""
    embed = discord.Embed(title = "Command: hug", color = 0xFFC0CB)
    if member is None:
        embed.description = f"{ctx.message.author.mention} has been hugged!"
    else:
        if member.id == ctx.message.author.id:
            embed.description = f"{ctx.message.author.mention} has hugged themself!"
        else:
            embed.description = f"{member.mention} has been hugged by {ctx.message.author.mention}!"
    await ctx.send(embed = embed)


@bot.command(aliases = ['say'])
async def echo(ctx, *msg):
    """Makes the bot talk."""
    try:
        await ctx.delete_message(ctx.message)
        await ctx.send(' '.join(msg))
    except:
        await ctx.send("If you managed to break this command, you are a fucking wizard or a hacker.")


@bot.command(name = "changeGame", aliases = ["gameChange", "changeActivity"])
async def change_game(ctx, *activity):
    """Changes what the bot is playing."""
    if ctx.message.author.guild_permissions.administrator:
        await bot.change_presence(activity =
                                  discord.Game(name = update_botsettings('currActivity', ' '.join(activity))))
        await ctx.send(embed = discord.Embed(title = "Command: changeGame", color = 0x0000FF,
                                             description = f"Game was changed to {' '.join(activity)}"))
    else:
        await ctx.send(embed = discord.Embed(title = "Command: changeGame", color = 0xFF0000,
                                             description = "You do not have permission to use this command!"))


@bot.command(name = "listGuilds", aliases = ["guilds", "guildList"])
async def list_guilds(ctx):
    """Shows how many guilds the bot is active on."""
    await ctx.send(embed = discord.Embed(title = "Command: listGuilds", color = 0x0000FF,
                                         description =
                                         '\n'.join([f"ID - {guild.id} : Name - {guild.name}" for guild in bot.guilds])))


@bot.command(name = "getBans", aliases = ["listBans", "bans"])
async def get_bans(ctx):
    """Lists all banned users on the current guild."""
    await ctx.send(embed = discord.Embed(title = "Command: getBans", color = 0x00FF00,
                                         description =
                                         '\n'.join([y.name for y in await ctx.get_bans(ctx.message.guild)])))


@bot.command(aliases = ['user'])
async def info(ctx, user: discord.Member):
    """Gets info on a member, such as their ID."""
    embed = discord.Embed(title = "Command: info", color = 0x0000FF)
    try:
        embed.add_field(name = "Name", value = user.name)
        embed.add_field(name = "ID", value = user.id)
        embed.add_field(name = "Joined at:", value = user.joined_at)
    except:
        embed.color = 0xFF0000
        embed.description("How did you fuck up this command?")
    await ctx.send(embed = embed)


@bot.command()
async def ping(ctx):
    """Pings the bot and gets a response time."""
    embed = discord.Embed(title = "Command: ping", color = 0x0000FF)
    try:
        pingtime = time.time()
        embed.description = "*Pinging...*"
        net_ping = (time.time() - pingtime) * 1000
        await ctx.edit_message(embed.description, f"**Pong!** Ping is `{net_ping:d}ms`")
    except:
        await ctx.send("How did you mess up the ping command? Just tell Xaereus.")


@bot.command(aliases = ['ud'])
async def urban(ctx, *msg):
    """Searches on the Urban Dictionary."""
    try:
        # Send request to the Urban Dictionary API and grab info
        response = requests.get("http://api.urbandictionary.com/v0/define", params = [("term", ' '.join(msg))]).json()
        embed = discord.Embed(description = "No results found!", color = 0xFF0000)
        if len(response["list"]) == 0:
            return await ctx.send(embed = embed)
        # Add results to the embed
        embed = discord.Embed(title = "Word", description = ' '.join(msg), color = embed.color)
        embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
        embed.add_field(name = "Examples:", value = response['list'][0]["example"])
        embed.set_footer(text = f"Tags: {', '.join(response['tags'])}")
        await ctx.send(embed = embed)

    except:
        await ctx.send("It done messed up.")


@bot.command()
async def load_initial(ctx):
    """Loads startup extensions."""
    if __name__ == "__main__":
        for extension_name in bot_settings['initial_extensions']:
            try:
                bot.load_extension(extension_name)
                await ctx.send(f"Loaded extension: '{extension_name}'")
            except Exception as e:
                print(f'Failed to load extension {extension_name}\n{type(e).__name__}: {e}')


@bot.command()
async def unload(ctx, extension_name: str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send(f"`{extension_name} unloaded.`")


@bot.command()
async def about(ctx):
    embed = discord.Embed(title = "Command: about", color = 0x0000FF)
    embed.add_field(name = "Name", value = bot.user.name)
    embed.add_field(name = "Built by", value = "Machoo and Xaereus")
    embed.add_field(name = "Running on", value = str(platform.platform()))
    embed.add_field(name = "Extensions", value = '\n'.join(f"**{x[5:]}**" for x in bot_settings['initial_extensions']))
    await ctx.send(embed = embed)


@bot.command(aliases = ['gh', 'code'])
async def github(ctx):
    """Gives you a link to the GitHub website."""
    await ctx.send("**GitHub:** https://github.com/BagelSnek/Cueball")


if __name__ == "__main__":
    for extension in bot_settings["initial_extensions"]:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension '{extension}'")
        except (AttributeError, ImportError) as e:
            print(f'Failed to load_initial extension {extension}\n{type(e).__name__}: {e}')

    bot.run(str(open('token.txt', 'r').read()))
