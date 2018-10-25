import discord
from discord.ext import commands
import json
import random


class TalkerCog:
    """TalkerCog is a cog that talks back. Sass included."""
    def __init__(self, bot):
        self.bot = bot

        with open('cogs/talkercog/responses.json') as responseJSON:
            self.responses = json.load(responseJSON)
        responseJSON.close()

    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith(self.bot.user.name):
            return await message.channel.send("You called?")
        if message.content.lower().startswith("hello"):
            return await message.channel.send(random.choice(self.responses["hello"]))
        if "are you single" in message.content.lower():
            return await message.channel.send(random.choice(self.responses["single"]))
        if "owo" in message.content.lower():
            return await message.channel.send("{0}{1}{0}".format(random.choice(self.responses['owo']['eye']),
                                                                 random.choice(self.responses['owo']['mouth'])))
        if "trigger" in message.content.lower():
            return await message.channel.send(random.choice(self.responses["triggered"]))


def setup(bot):
    bot.add_cog(TalkerCog(bot))
