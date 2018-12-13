import nltk
import random
from rstr import xeger
from copy import deepcopy
from cogs.utils.dataIO import dataIO
from cogs.utils.text_formatter import txt_frmt
from cogs.utils.settings import settings
import discord
from discord.ext import commands


class TalkerCog:
    """
    TalkerCog is a cog that talks back. Sass included, batteries not included.
    -- Designed for use with Cueball --
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.responses = dataIO.load_json('conversation/responses.json')
        self.personalized = dataIO.load_json('conversation/personalized.json')

    @staticmethod
    def check_response(message, responses):
        """Loops through the responses dict and returns the first valid response."""
        for resp in responses.values():
            if txt_frmt.regscan(message.content, resp['settings']['regex'], clean_str = bool('clean' not in resp['settings'])):

                # Setting the delete_after if it is in the dict
                del_aft = resp['settings']['delete_after'] if 'delete_after' in resp['settings'] else None

                # Running checks in the dict if it exists, else it just passes
                if 'checks' in resp['settings']:
                    if not eval(resp['settings']['checks']):
                        return None
                if type(resp['responses']) == str:
                    # Creates string that matches the regex given.
                    return {'response': xeger(resp['responses']), 'delete_after': del_aft}
                return {'response': random.choice(resp['responses']), 'delete_after': del_aft}

        return None

    async def on_message(self, message):
        if any(prefix in message.content for prefix in settings.get_prefixes(message.guild)) \
                or message.author == self.bot.user:
            return

        responses = deepcopy(self.responses)
        personalized = deepcopy(self.personalized)

        # Personalized response checker.
        if str(message.author.id) in self.personalized:
            if "ignored" in self.personalized[str(message.author.id)]:
                return

            dataIO.merge(responses, personalized[str(message.author.id)])

        response = self.check_response(message, responses)

        if response is not None:
            await message.channel.send(response['response'], delete_after = response['delete_after'])

    @commands.command(aliases = ["bigitize", "bigicate", "biginate", "enlarge"])
    async def bigify(self, ctx, *message: str):
        """Send a large, emoji constructed message of whatever sentence you want."""
        await ctx.message.delete()
        await ctx.send("".join([f":regional_indicator_{letter}:" if letter != " " else "   " for letter in
                               [char for char in txt_frmt.clean(' '.join(message))]]))

    @commands.command(aliases = ['say'])
    async def echo(self, ctx, *say):
        """Makes the bot talk."""
        try:
            await ctx.message.delete()
            await ctx.send(' '.join(say))
        except:
            await ctx.send("If you managed to break this command, you are a fucking wizard or a hacker.")

    @commands.command()
    async def answer(self, ctx, *question: str):
        """Answers a basic question."""
        embed = discord.Embed(title = "Command: answer", color = 0x0000FF, description = " ".join(question))
        questions = txt_frmt.clean(" ".join(question)).split(' or ')
        if len(questions) == 1:
            embed.set_footer(text =
                             random.choice(["yes", "yas", "yep", "yup", "no", "nop", "nope", "noperino"]).capitalize())
        else:
            for chunk in questions:
                for word, tag in nltk.pos_tag(nltk.tokenize.word_tokenize(chunk), tagset = 'universal'):
                    if tag == 'PRON' or word == 'should':
                        chunk.replace(word, '')
            embed.set_footer(text = random.choice(questions).capitalize())
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(TalkerCog(bot))
