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
        if message.author.bot:
            return

        clean_msg = re.sub(r'([^a-z0-9\s])', '', message.content.lower())

        if clean_msg.startswith(self.bot.user.name.lower()) or message.content == self.bot.user.mention:
            return await message.channel.send(random.choice(self.responses['mentioned']))
        if len(set(self.responses['hello']['prompts']).intersection(set(clean_msg.split(' ')))) > 0:
            return await message.channel.send(random.choice(self.responses['hello']['responses']))
        if bool(re.search(r"\A(are)|r (you)|u single\Z", clean_msg)):
            return await message.channel.send(random.choice(self.responses['single']))
        if bool(re.search(r"\b(?P<eye>[@oO0u^;.,x])(?P<mouth>[_\-wW=~km3])(?P=eye)\b", message.content)):
            return await message.channel.send("{0}{1}{0}".format(random.choice(self.responses['owo']['eye']),
                                                                 random.choice(self.responses['owo']['mouth'])))
        if "trigger" in clean_msg:
            return await message.channel.send(random.choice(self.responses['triggered']))
        if len(set(self.responses['boop']).intersection(set(clean_msg.split(' ')))) > 0:
            return await message.channel.send(random.choice(self.responses['boop']).capitalize() + "!")
        if "oof" in clean_msg:
            return await message.channel.send(random.choice(self.responses['oof']))
        if "bye" in clean_msg:
            return await message.channel.send(random.choice(self.responses['bye']))
        if "no u" in clean_msg:
            return await message.channel.send(random.choice(self.responses['no u']))
        if "kachigga" in clean_msg:
            return await message.channel.send(random.choice(self.responses['kachigga']))
        if "connor" in clean_msg:
            return await message.channel.send("*They said senpai-san's name!* :hearts:", delete_after = 5)


def setup(bot):
    bot.add_cog(TalkerCog(bot))
