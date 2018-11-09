import json
import random
import re
import os


class TalkerCog:
    """TalkerCog is a cog that talks back. Sass included."""

    def __init__(self, bot):
        self.bot = bot

        # Basic responses.
        with open('cogs/talkercog/responses.json') as responseJSON:
            self.responses = json.load(responseJSON)
        responseJSON.close()

        # Personalized responses for members in personalized.json.
        if not os.path.isfile('cogs/talkercog/personalized.json'):
            self.personalized = {"members": {}}
        else:
            with open('cogs/talkercog/personalized.json') as personalizedJSON:
                self.personalized = json.load(personalizedJSON)
            personalizedJSON.close()

    async def on_message(self, message):
        if self.bot.command_prefix in message.content:
            return

        clean_msg = re.sub(r'[^a-z0-9\s]+', '', message.content.lower())

        response = None
        delete_after = None
        responses = self.responses

        # Personalized response checker.
        if str(message.author.id) in list(self.personalized['members'].keys()):
            if "ignored" in list(self.personalized['members'][str(message.author.id)].keys()):
                return

            for key in list(self.personalized['members'][str(message.author.id)].keys()):
                if key in responses:
                    print(type(responses[key]))
                    (responses[key]).update(self.personalized['members'][str(message.author.id)][key])
                else:
                    responses[key] = self.personalized['members'][str(message.author.id)][key]

        # Standard responses.
        if len(set(self.responses['hello']['prompts']).intersection(
               set(clean_msg.replace("hey ", "hey").replace("whats ", "whats").split(' ')))) > 0:
            response = random.choice(responses['hello']['responses'])

        elif 6 <= message.created_at.hour <= 17 and "goodmorning" in re.sub(r'\s', '', clean_msg):
            response = random.choice(responses['hello']['morning'])

        elif 0 <= message.created_at.hour <= 5 and "goodnight" in re.sub(r'\s', '', clean_msg):
            response = random.choice(responses['hello']['night'])

        elif bool(re.search(r"\A((are )|(r ))+((you )|(u ))+(single)+\Z", clean_msg)):
            response = random.choice(responses['single'])

        elif bool(re.search(r"(?P<eye>[@o0u^;.,x])[_w=~m3-](?P=eye)", message.content.lower())):
            response = "{0}{1}{0}".format(random.choice(responses['owo']['eye']),
                                          random.choice(responses['owo']['mouth']))

        elif "trigger" in clean_msg:
            response = random.choice(responses['triggered'])

        elif bool(re.search(r"bw*[aeo]+p", clean_msg)):
            response = random.choice(responses['boop'])

        elif "oof" in clean_msg:
            response = random.choice(responses['oof'])

        elif "bye" in clean_msg:
            response = random.choice(responses['bye'])

        elif "no u" in clean_msg:
            response = random.choice(responses['no u'])

        elif "kachigga" in clean_msg:
            response = random.choice(responses['kachigga'])

        elif "connor" in clean_msg:
            response = random.choice(responses['crush'])
            delete_after = 3

        elif clean_msg.startswith(self.bot.user.name.lower()) or message.content == self.bot.user.mention:
            response = random.choice(responses['mentioned'])

        if response is not None:
            await message.channel.send(response, delete_after = delete_after)

        # "%r"%"non literal string"
        # eval("r'%s'" % (raw_input(),))
        # re.search(r"\b(?<=\w)" + TEXTO + "\b(?!\w)", subject, re.IGNORECASE)


def setup(bot):
    bot.add_cog(TalkerCog(bot))
