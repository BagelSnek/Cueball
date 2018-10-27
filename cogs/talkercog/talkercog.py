import json
import random
import re


class TalkerCog:
    """TalkerCog is a cog that talks back. Sass included."""
    def __init__(self, bot):
        self.bot = bot

        with open('cogs/talkercog/responses.json') as responseJSON:
            self.responses = json.load(responseJSON)
        responseJSON.close()

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        clean_msg = re.sub('\W+', ' ', message.content.lower())

        if clean_msg.startswith(self.bot.user.name.lower()):
            return await message.channel.send("You called?")
        if clean_msg.startswith("hello"):
            return await message.channel.send(random.choice(self.responses['hello']))
        if "are you single" in clean_msg:
            return await message.channel.send(random.choice(self.responses['single']))
        if bool(re.search(r"\b(?P<eye>[@oO0u^;.,x])(?P<mouth>[_\-wW=~km3])(?P=eye)\b", message.content)):
            return await message.channel.send("{0}{1}{0}".format(random.choice(self.responses['owo']['eye']),
                                                                 random.choice(self.responses['owo']['mouth'])))
        if "trigger" in clean_msg:
            return await message.channel.send(random.choice(self.responses['triggered']))
        if len(set(self.responses['boop']).intersection(set(clean_msg.split(' ')))) > 0:
            return await message.channel.send(random.choice(self.responses['boop']).capitalize() + "!")


def setup(bot):
    bot.add_cog(TalkerCog(bot))
