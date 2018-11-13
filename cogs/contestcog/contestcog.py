import os
import random
import discord
import datetime
import json
from functools import reduce
import aiocron
import asyncio


class ContestCog(discord.Client):
    """ContestCog is a cog that manages a weekly contest in any channel named 'weekly-contest'."""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.bg_task = self.loop.create_task(self.contest())
        self._update_cron = aiocron.crontab('1 0 * * *', func = self.contest, start = True)
        self.is_active_contest = False

        if not os.path.isfile('cogs/contestcog/contesthistory.json'):
            print("Making contesthistory.json.")
            json.dump({"contests": []}, open('cogs/contestcog/contesthistory.json', 'w'), indent = 2)
        else:
            with open('cogs/contestcog/contesthistory.json', 'r') as contest_history:
                self.contest_history = json.load(contest_history)
            contest_history.close()

        with open('cogs/contestcog/contests.json', 'r') as contests:
            self.contests = json.load(contests)
        contests.close()

    # Alloy only one vote, remove new vote if one is already present.
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        user = self.bot.get_user(payload.user_id)
        if channel.name != "weekly-contest" or self.bot.get_user(payload.user_id) == self.bot.user:
            return

        # Delete reaction if the user has voted in that channel before or is a bot other than Cueball.
        if [member.id for member in list(filter(None, reduce(lambda x, y: x + y,  [await react.users().flatten()
           if react.emoji == self.bot.get_emoji(509383247772385311) else None for react in reduce(lambda x, y: x + y,
           [message.reactions for message in await channel.history().flatten()])])))].count(user.id) > 1 or user.bot:

            message = await channel.get_message(payload.message_id)
            await message.remove_reaction(payload.emoji, user)

    # Allow only one submition for competion and delete submition is one is present.
    async def on_message(self, message):
        if message.channel.name != "weekly-contest" or message.author == self.bot.user:
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

        if self.contest_history['contests']:
            self.contests['challenges'].remove(self.contest_history['contests'][-1]['challenge'])

        contest = {"date": datetime.date.today().strftime('%y/%m/%d'),
                   "challenge": random.choice(self.contests['challenges'])}
        self.contest_history['contests'].append(contest)
        json.dump(self.contest_history, open('cogs/contestcog/contesthistory.json', 'w'), indent = 2)

        for channel in channels:
            chanhist = await channel.history(limit = None, reverse = True).flatten()
            if chanhist:
                await channel.delete_messages(chanhist)
            await channel.send(f"**Entertain me, mortals.** {contest['challenge']} you can in this channel!\n"
                               f"Vote on your favorite with {self.bot.get_emoji(509383247772385311)}. The most "
                               f"votes before Sunday wins!\n"
                               "Post only once, I don't wanna have to delete messages. Same goes for votes.\n"
                               "Don't vote for yourself, by the way.")

        self.is_active_contest = True
        print("\tNew contest started.")

    async def end_contest(self, channels):
        """Ends previous contest."""

        print("\tEnding previous contest...")

        for channel in channels:
            tally = {}
            for message in await channel.history().flatten():
                if not await channel.history().flatten():
                    pass
                elif not message.author.bot:
                    tally[str(message.author.id)] = [react.count if react.emoji.id == 509383247772385311
                                                     else 0 for react in message.reactions][0]

            # Tally up winners if there are any.
            winners = [self.bot.get_user(int(key)).mention for key in tally if tally[key] == max(tally.values())] if tally else []

            if len(winners) == 0:
                response = "No winners this week."
            elif len(winners) > 1:
                response = f"{', '.join(winners[:-1])} and {winners[-1]} won!"
            else:
                response = f"{winners[0]} won!"

            # Add code to send the submition for each user in response.

            await channel.delete_messages(await channel.history(limit = None).flatten())
            await channel.send(response)

            self.is_active_contest = False
            print("\tPrevious contest ended.")

    async def contest(self):
        """Runs contests."""
        await self.bot.wait_until_ready()
        await asyncio.sleep(2)

        print("Checking contest...")

        # Assemble channel list for contests
        channels = list(filter(None, [channel if "weekly-contest" in channel.name
                                      else None for channel in self.bot.get_all_channels()]))
        previous_contest = self.contest_history['contests'][-1]['date']

        # Friday's code
        if datetime.datetime.today().weekday() == 4 and not self.is_active_contest and \
                previous_contest != datetime.datetime.today().strftime('%y/%m/%d'):
            await self.start_contest(channels)
        # Sunday's code
        elif datetime.datetime.today().weekday() == 6 and self.is_active_contest and \
                previous_contest == (datetime.datetime.today() - datetime.timedelta(days = 2)).strftime('%y/%m/%d'):
            await self.end_contest(channels)

        print("Contest checked.\n")


def setup(bot):
    bot.add_cog(ContestCog(bot))
