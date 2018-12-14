import random
import datetime
from functools import reduce
import aiocron
import asyncio
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils.text_formatter import txt_frmt


class ContestCog:
    """
    ContestCog is a cog that manages a weekly contest in any channel named 'weekly-contest'.
    -- Designed for use with Cueball --
    """

    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.contest())
        self._update_cron = aiocron.crontab('1 0 * * *', func = self.contest, start = True)
        self.is_active_contest = False

        # Make update command to check values in contesthistory.json later.
        self.contest_history = dataIO.load_json('contests/contesthistory.json')
        self.contests = dataIO.load_json('contests/contests.json')

        if not self.contest_history:
            self.contest_history = {"contests": []}

    # Alloy only one vote, remove new vote if one is already present.
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        user = self.bot.get_user(payload.user_id)
        if channel.name != "weekly-contest" or self.bot.get_user(payload.user_id) == self.bot.user:
            return

        if (payload.emoji.id != 509383247772385311 and self.is_active_contest) or user.bot:
            message = await channel.get_message(payload.message_id)
            await message.remove_reaction(payload.emoji, user)

        user_list = txt_frmt.deblank([await react.users().flatten()
                   if react.emoji == self.bot.get_emoji(509383247772385311) else None for react in reduce(lambda x, y: x + y,
                   [message.reactions for message in await channel.history().flatten()])])

        # Delete reaction if the user has voted in that channel before or is a bot other than Cueball.
        if len(user_list) != 0:
            if [member.id for member in reduce(lambda x, y: x + y,  user_list)].count(user.id) > 1:

                message = await channel.get_message(payload.message_id)
                await message.remove_reaction(payload.emoji, user)

    # Allow only one submition for competion and delete submition is one is present.
    async def on_message(self, message):
        if txt_frmt.clean(message.channel.name) != "weeklycontest" or message.author == self.bot.user:
            return

        # Delete message if the author already sent one in this channel or is a bot other than Cueball. Else, add vote.
        if [msg.author.id for msg in await message.channel.history().flatten()].count(message.author.id) > 1 \
                or message.author.bot or not self.is_active_contest:
            await message.delete()
        else:
            await message.add_reaction(self.bot.get_emoji(509383247772385311))

    async def start_contest(self, channels):
        """Starts a new random contest for every channel in channels if it is not in the log."""

        print("\tStarting new contest...")

        # Makes sure that contests are not repeated within a 2 week timespan.
        if len(self.contest_history['contests']) > 1:
            challenges = list(set(self.contests['challenges']) -
                              {x['challenge'] for x in self.contest_history['contests'][-2:]})
        else:
            challenges = self.contests['challenges']

        # Defines and logs contest.
        contest = {"date": datetime.date.today().strftime('%y/%m/%d'),
                   "challenge": random.choice(challenges)}
        self.contest_history['contests'].append(contest)
        dataIO.dump_json('contests/contesthistory.json', self.contest_history)

        for channel in channels:
            print(f"\t\tAttempting to start contest in {channel.guild.name}...")
            try:
                chanhist = await channel.history(limit = None, reverse = True).flatten()
                if chanhist:
                    await channel.delete_messages(chanhist)
                await channel.send(f"**Entertain me, mortals.** {contest['challenge']} you can in this channel!\n"
                                   f"Vote on your favorite with {self.bot.get_emoji(509383247772385311)}. The most "
                                   "votes before Sunday wins!\n"
                                   "Post only once, I don't wanna have to delete messages. Same goes for votes.\n"
                                   "Don't vote for yourself, by the way.")
                print(f"\t\tContest successfully started in {channel.guild.name}.")
            except commands.MissingPermissions as exc:
                print(f"\t\tError when trying to start contest in {channel.guild.name}.\n"
                      f"\t\t{type(exc).__name__} : {exc}")

        self.is_active_contest = True
        print("\tNew contest started.")

    async def end_contest(self, channels):
        """Ends previous contest."""

        print("\tEnding previous contest...")

        for channel in channels:
            print(f"\t\tAttempting to end contest in {channel.guild.name}...")
            channel_hist = await channel.history(limit = None).flatten()
            try:
                tally = {}
                for message in channel_hist:
                    if not channel_hist:
                        pass
                    elif not message.author.bot:
                        tally[str(message.author.id)] = txt_frmt.deblank([react.count if react.emoji.id == 509383247772385311
                                                                 else None for react in message.reactions])[0]

                # Tally up winners if there are any.
                winners = [self.bot.get_user(int(key)) for key in tally if tally[key] == max(tally.values())] if tally else []

                if len(winners) == 0:
                    response = "No winners this week."
                elif len(winners) > 1:
                    response = f"{', '.join([winner.mention for winner in winners[:-1]])}" \
                               f" and {winners[-1].mention} won!"
                else:
                    response = f"{winners[0].mention} won!"

                if winners and channel_hist:
                    for message in channel_hist:
                        if message.author in winners:
                            content = f"```{message.content}```" if not message.attachments else message.attachments[0]
                            response += f"\n\n**{message.author.name}**\n{content}"

                await channel.delete_messages(channel_hist)
                await channel.send(response)
            except commands.MissingPermissions as exc:
                print(f"\t\tError when trying to end contest in {channel.guild.name}.\n"
                      f"\t\t{type(exc).__name__} : {exc}")

        self.is_active_contest = False
        print("\tPrevious contest ended.")

    async def contest(self):
        """Runs contests."""
        await self.bot.wait_until_ready()
        await asyncio.sleep(5)

        print("Checking contest...")

        # Assembles channel list for contests.
        channels = txt_frmt.deblank([channel if txt_frmt.clean(channel.name) == "weeklycontest"
                            else None for channel in self.bot.get_all_channels()])
        previous_contest = self.contest_history['contests'][-1]['date'] if self.contest_history['contests'] else None

        # Friday's code.
        if datetime.datetime.today().weekday() == 4 and not self.is_active_contest and \
                previous_contest != datetime.datetime.today().strftime('%y/%m/%d'):
            await self.start_contest(channels)

        # Sunday's code.
        elif datetime.datetime.today().weekday() == 6 and self.is_active_contest and \
                previous_contest == (datetime.datetime.today() - datetime.timedelta(days = 2)).strftime('%y/%m/%d'):
            await self.end_contest(channels)

        print("Contest checked.\n")


def setup(bot):
    bot.add_cog(ContestCog(bot))
