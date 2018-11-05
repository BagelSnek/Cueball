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

        clean_msg = re.sub(r'[^a-z0-9\s]+', '', message.content.lower())

        if len(set(self.responses['hello']['prompts']).intersection(set(clean_msg.split(' ')))) > 0:
            if message.author.id == 401139202487746562:
                return await message.channel.send("Hi, thot.")
            return await message.channel.send(random.choice(self.responses['hello']['responses']))

        if 6 <= message.created_at.hour <= 17 and "goodmorning" in re.sub(r'\s', '', clean_msg):
            return await message.channel.send(random.choice(self.responses['hello']['morning']))

        if 0 <= message.created_at.hour <= 5 and "goodnight" in re.sub(r'\s', '', clean_msg):
            return await message.channel.send(random.choice(self.responses['hello']['night']))

        if bool(re.search(r"(are )|(r )(you )|(u )(single)\Z", clean_msg)):
            return await  message.channel.send(random.choice(self.responses['single']))

        if bool(re.search(r"\b(?P<eye>[@oO0u^;.,x])(?P<mouth>[_w=~km3-])(?P=eye)\b", message.content)):
            return await message.channel.send("{0}{1}{0}".format(random.choice(self.responses['owo']['eye']),
                                                                 random.choice(self.responses['owo']['mouth'])))

        if "trigger" in clean_msg:
            return await message.channel.send(random.choice(self.responses['triggered']))

        if bool(re.search(r"bw*[aeo]+p", clean_msg)):
            return await message.channel.send(random.choice(self.responses['boop']))

        if "oof" in clean_msg:
            return await message.channel.send(random.choice(self.responses['oof']))

        if "bye" in clean_msg:
            return await message.channel.send(random.choice(self.responses['bye']))

        if "no u" in clean_msg:
            return await message.channel.send(random.choice(self.responses['no u']))

        if "kachigga" in clean_msg:
            return await message.channel.send(random.choice(self.responses['kachigga']))

        if "connor" in clean_msg:
            return await message.channel.send("*They said Connor-senpai's name!* :hearts:", delete_after = 3)

        if clean_msg.startswith(self.bot.user.name.lower()) or message.content == self.bot.user.mention:
            return await message.channel.send(random.choice(self.responses['mentioned']))


def setup(bot):
    bot.add_cog(TalkerCog(bot))
