import discord
from discord.ext import commands


class SocialCog:
    """SocialCog is a cog that interacts with the people on the server and facilitates interaction between members."""
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


def setup(bot):
    bot.add_cog(SocialCog(bot))
