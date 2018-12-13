import datetime
import os
import platform
import subprocess
import discord
from discord.ext import commands
from cogs.utils.settings import settings
from cogs.utils import checks
import git


class ModCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['remove', 'delete'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int):
        """
        Bulk-deletes messages from the channel.
        """

        await ctx.message.channel.delete_messages(await ctx.channel.history(limit = amount).flatten())

    @commands.command(name = "changeGame", aliases = ["gameChange", "changePlaying", "changeActivity"])
    @checks.is_auth()
    async def change_game(self, ctx, *game):
        """
        Changes what the bot is playing.
        """

        game = ' '.join(game)
        settings.bot_settings['currActivity'] = game
        settings.save_bot_settings()
        await self.bot.change_presence(activity = discord.Game(name = game))
        await ctx.send(embed = discord.Embed(title = "Command: changeActivity", color = 0x0000FF,
                                             description = f"Game was changed to {game}"))

    @commands.command()
    async def ping(self, ctx):
        """
        Pings the bot and gets a response time.
        """

        embed = discord.Embed(title = "Command: ping", color = 0x0000FF)
        try:
            embed.description = str(round(self.bot.latency * 100, 4)) + "ms"
            await ctx.send(embed = embed)
        except:
            await ctx.send("How did you mess up the ping command? Just tell Xaereus.")

    @commands.command()
    @checks.is_auth()
    async def load(self, ctx, extension_name: str):
        """
        Loads an extension/cog.
        """

        try:
            if extension_name in settings.extensions.keys():
                self.bot.load_extension(f"cogs.{extension_name}")
                settings.enable_extension(extension_name)
                await ctx.send(f"Loaded extension: `{extension_name}`")
            else:
                await ctx.send(f"`{extension_name}` is not a valid extension!")
        except (discord.ClientException, ImportError) as exc:
            await ctx.send(f"Failed to load extension {extension_name}\n{type(exc).__name__}: {exc}")

    @commands.command()
    @checks.is_auth()
    async def unload(self, ctx, extension_name: str):
        """
        Unloads an extension/cog.
        """

        try:
            if extension_name in settings.extensions.keys():
                self.bot.unload_extension(f"cogs.{extension_name}")
                settings.disable_extension(extension_name)
                await ctx.send(f"Unloaded extension: `{extension_name}`")
            else:
                await ctx.send(f"`{extension_name}` is not a valid extension!")
        except (discord.ClientException, ImportError) as exc:
            await ctx.send(f"Failed to unload extension {extension_name}\n{type(exc).__name__}: {exc}")

    @commands.command()
    async def about(self, ctx):
        """
        Displays various information about the bot.
        """

        embed = discord.Embed(title = "Command: about", color = 0x0000FF)
        embed.add_field(name = "Name", value = self.bot.user.name)
        embed.add_field(name = "Built by", value = "Machoo and Xaereus")
        embed.add_field(name = "Running on", value = str(platform.platform()))
        embed.add_field(name = "Github", value = "https://github.com/BagelSnek/Cueball")
        embed.add_field(name = "Servers", inline = False,
                        value = "\n".join([f"`ID - {guild.id} : Name - {guild.name}`" for guild in self.bot.guild_ids]))

        cogs = dict(self.bot.settings['extensions'])
        if cogs:
            embed.add_field(name = "Loaded extensions",
                            value = '\n'.join(list(filter(None, [f"`{cog['alias']}`" if cog['status'] == "loaded"
                                                                 else None for cog in cogs.values()]))))
        await ctx.send(embed = embed)

    @commands.command(name = "uptime")
    async def uptime(self, ctx):
        await ctx.send(datetime.datetime.utcnow() - self.bot.uptime)

    @checks.is_auth()
    @commands.command()
    async def reboot(self, ctx):
        """
        Reboots script if the user is authorized.
        """
        await ctx.send("Rebooting!")
        await self.bot.logout()

    @checks.is_auth()
    @commands.command(name = 'update')
    async def update_cue(self, ctx, reboot = "false"):
        try:
            repo = git.Repo()
            repo.remotes.origin.pull(rebase = True)

            await ctx.send("Update successful!")

            if reboot == "true":
                await self.reboot(ctx)
        except:
            await ctx.send("An error occurred whilst attempting to update.")



def setup(bot):
    bot.add_cog(ModCog(bot))
