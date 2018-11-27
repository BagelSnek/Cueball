import random
from copy import deepcopy
from utils import utils
from rstr import xeger
from discord.ext import commands
from re import sub


class TalkerCog:
    """TalkerCog is a cog that talks back. Sass included, batteries not included."""

    def __init__(self, bot):
        self.bot = bot

        self.responses = utils.load_json('cogs/talkercog/responses.json')
        self.personalized = utils.load_json('cogs/talkercog/personalized.json')

    @staticmethod
    def check_response(message, responses):
        """Loops through the responses dict and returns the first valid response."""
        for resp in responses.values():
            if utils.reg_searcher(message.content, resp['settings']['regex'],
                                  clean = bool('clean' not in resp['settings'])):

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
        if self.bot.command_prefix in message.content or message.author == self.bot.user:
            return

        responses = deepcopy(self.responses)
        personalized = deepcopy(self.personalized)

        # Personalized response checker.
        if str(message.author.id) in self.personalized:
            if "ignored" in self.personalized[str(message.author.id)]:
                return

            utils.merge(responses, personalized[str(message.author.id)])

        response = self.check_response(message, responses)

        if response is not None:
            await message.channel.send(response['response'], delete_after = response['delete_after'])

    @commands.command(aliases = ["bigitize", "bigicate", "biginate", "enlarge"])
    async def bigify(self, ctx, *message: str):
        """Send a large, emoji constructed message of whatever sentence you want."""
        await ctx.message.delete()
        await ctx.send("".join([f":regional_indicator_{letter}:" if letter != " " else "   " for letter in
                               [char for char in sub(r'([^a-z0-9\s])+', '', ' '.join(message).lower())]]))

    @commands.command(aliases = ['say'])
    async def echo(self, ctx, *say):
        """Makes the bot talk."""
        try:
            await ctx.message.delete()
            await ctx.send(' '.join(say))
        except:
            await ctx.send("If you managed to break this command, you are a fucking wizard or a hacker.")


def setup(bot):
    bot.add_cog(TalkerCog(bot))
