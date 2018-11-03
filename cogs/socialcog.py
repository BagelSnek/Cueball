import re
import discord
from discord.ext import commands


class SocialCog:
    """SocialCog is a cog that facilitates interaction between members, good or bad."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hug(self, ctx, *, member: discord.Member = None):
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

    @commands.command(aliases = ["fuckingbeat"])
    async def beat(self, ctx, *, member: discord.Member = None):
        """Fucking beat someone. -Requested by Balasar"""
        embed = discord.Embed(title = "Command: beat", color = 0x00FF90)
        if member is None:
            embed.description = "Choose a foolio to beat, kachigga."
        else:
            if member.id == ctx.message.author.id:
                embed.description = f"{ctx.message.author.mention} beat themself up...?"
            else:
                embed.description = f"{ctx.message.author.mention} fucking beat {member.mention}!"
        await ctx.send(embed = embed)

    @commands.command(aliases = ["bigitize", "bigicate", "biginate", "enlarge"])
    async def bigify(self, ctx, *message: str):
        """Send a large, emoji constructed message of whatever sentence you want."""
        await ctx.message.delete()
        await ctx.send("".join([f":regional_indicator_{letter}:" if letter != " " else "   " for letter in
                               [char for char in re.sub(r'([^a-z0-9\s])+', '', ' '.join(message).lower())]]))

    @commands.command(aliases = ['say'])
    async def echo(self, ctx, *say):
        """Makes the bot talk."""
        try:
            await ctx.message.delete()
            await ctx.send(' '.join(say))
        except:
            await ctx.send("If you managed to break this command, you are a fucking wizard or a hacker.")


def setup(bot):
    bot.add_cog(SocialCog(bot))
