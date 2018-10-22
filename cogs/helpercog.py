from discord.ext import commands
import discord
import inspect


class HelperCog:
    """HelperCog is a cog that deals with the help commands in a more intuative way than the default help command."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command
    async def help(self, ctx, query: str = None):
        f"""This is the Cueball help page. Below should be a list of all commands that you can use in the main bot
        and each cog loaded. to reference this again, type `{self.bot.command_prefix}help`. If you want to get the
        help for a specific command, use `{self.bot.command_prefix}help <command>`."""

        embed = discord.Embed(title = "Command: help", color = 0xFFFFFF)
        if query is not None:
            if self.bot.get_command(query) is None:
                embed.color = 0xFF0000
                embed.description = "The command you\'re looking for was not found. " \
                                    f"Use `{self.bot.command_prefix}help` to get a list of availible commands."
            else:
                embed.description = self.bot.get_command(query)['callback'].__doc__
        else:
            embed = discord.Embed(title = "Command: help", description = __doc__)
            cogs = list(set([command.cog_name if command.cog_name is not None
                             else "Main" for command in self.bot.commands]))
            for cog in cogs:
                embed.add_field(name = cog, value =
                                "\n".join([f"'{self.bot.command_prefix}{command['trigger']}` " + (f"`<{param.name}>` "
                                           if param.default is not inspect.Parameter.empty else f'`[{param.name}]` ')
                                           if param.name != "ctx" and param.name != "self" else ""
                                           for command in self.bot.commands
                                           for param in inspect.Signature(command['callback']).parameters]))
        ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(HelperCog(bot))
