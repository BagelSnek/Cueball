import discord
from discord.ext import commands


class LuckyCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "8ball")
    async def _8ball(self, ctx, *question: str):
        embed = discord.Embed(title = "Command: 8ball", color = 0x000000)
        embed.set_footer(text = " ".join(question))
        ctx.send(embed = embed)
