import discord
from discord.ext import commands


class SocialCog:
    """
    SocialCog is a cog that facilitates interaction between members, good or bad.
    -- Designed for use with Cueball --
    """
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

    @commands.command(aliases = ['user', 'whois'])
    async def info(self, ctx, user: discord.Member):
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

    @commands.command(name = "getBans", aliases = ["listBans", "bans"])
    async def get_bans(self, ctx):
        """Lists all banned users on the current guild."""
        await ctx.send(embed = discord.Embed(title = "Command: getBans", color = 0x00FF00,
                                             description =
                                             '\n'.join([y.name for y in await ctx.get_bans(ctx.guild)])))

    @commands.command(name = "listRoles", aliases = ["roles"])
    async def list_roles(self, ctx):
        """Lists the current roles on the guild."""
        await ctx.send(embed = discord.Embed(title = "Command: listRoles", color = 0x0000FF,
                                             description = "\n".join(filter(None, [f"`{role.name}`"
                                                                                   if role.name != "@everyone" else None
                                                                                   for role in
                                                                                   ctx.guild.roles]))))


def setup(bot):
    bot.add_cog(SocialCog(bot))
