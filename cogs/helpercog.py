from discord import Embed
from discord.ext import commands
import inspect
from cogs.utils.settings import settings


class HelperCog:
    """
    HelperCog is a cog that deals with the help commands in a more intuative way than the default help command.
    -- Designed for use with Cueball --
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "help")
    async def help(self, ctx, query: str = None):
        """
        This is the Cueball help page! Below is a list of all commands that you can use in the main bot and each
        cog loaded. To reference this again, use `help`, and if you want to get the help for a specific command,
        use `help <command>`.
        Prefixes for this guild: `{}`
        """

        embed = Embed(title = "Command: help", color = 0xFFFFFF)
        prefixes = settings.get_prefixes(ctx.guild)
        if query is not None:
            if self.bot.get_cog(query) is None:
                if self.bot.get_command(query) is None:
                    embed.color = 0xFF0000
                    embed.description = "The command you\'re looking for was not found. " \
                                        f"Use `help` to get a list of availible commands."
                else:
                    embed.description = f"{self.bot.get_command(query).name} : " \
                                        f"{str(self.bot.get_command(query).callback.__doc__)}"
                    if len(self.bot.get_command(query).aliases) > 0:
                        embed.add_field(name = "Aliases", inline = False,
                                        value = "\n".join(self.bot.get_command(query).aliases))
            else:
                embed.description = self.bot.get_cog(query).__doc__
        else:
            embed.description = str(self.bot.get_command('help').callback.__doc__).format("  ".join(prefixes))
            cogs = list(set([command.cog_name for command in self.bot.commands]))
            for cog in cogs:
                embed.add_field(name = cog if cog is not None else "Main", inline = False, value =
                                "\n".join(filter(None, [(f"`{command.name}` " + " ".join([f"`[{param.name}]`"
                                           if param.default is not inspect.Parameter.empty else f"`<{param.name}>` "
                                           if param.name != "ctx" and param.name != "self" else ""
                                           for param in inspect.signature(command.callback).parameters.values()]))
                                           if command.cog_name == cog else "" for command in self.bot.commands])))
        await ctx.send(embed = embed)


def setup(bot):
    bot.remove_command('help')
    bot.add_cog(HelperCog(bot))
