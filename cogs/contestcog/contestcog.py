import os
import random
import discord
import datetime
import json
from functools import reduce
import aiocron


class ContestCog(discord.Client):
    """ContestCog is a cog that manages a weekly contest in any channel named 'weekly-contest'."""

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.bg_task = self.loop.create_task(self.contest())
        self._update_cron = aiocron.crontab('1 0 * * 4,6', func = self.contest, start = True)

        if not os.path.isfile('cogs/contestcog/contesthistory.json'):
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
        if channel.name != "weekly-contest" or self.bot.get_user(payload.user_id).bot or payload.emoji != self.bot.get_emoji(509383247772385311):
            return

        if [member.id for member in list(filter(None, reduce(lambda x, y: x + y,  [await react.users().flatten()
           if react.emoji == self.bot.get_emoji(509383247772385311) else None for react in reduce(lambda x, y: x + y,
           [message.reactions for message in await channel.history().flatten()])])))].count(payload.user_id) > 1:

            message = await channel.get_message(payload.message_id).remove_reaction(payload.emoji, self.bot.get_user(payload.user_id))
            await message.remove_reaction(payload.emoji, self.bot.get_user(payload.user_id))

    # Allow only one submition for competion and delete submition is one is present.
    async def on_message(self, message):
        if message.channel.name != "weekly-contest" or message.author.bot:
            return

        if [msg.author.id for msg in await message.channel.history().flatten()].count(message.author.id) > 1:
            await message.delete()
        else:
            await message.add_reaction(self.bot.get_emoji(509383247772385311))

    async def contest(self):
        await self.bot.wait_until_ready()

        # Assemble channel list for contests and stop method if the weekday isn't 4 or 6.
        channels = list(filter(None, [channel if "weekly-contest" in channel.name
                                      else None for channel in self.bot.get_all_channels()]))

        # Log contest and send message in channels marked as contest channels.
        if datetime.datetime.today().weekday() == 4:
            self.contests['challenges'].remove(self.contest_history['contests'][-1]['challenge'])
            contest = {"date": datetime.date.today().strftime('%y/%m/%d'),
                       "challenge": random.choice(self.contests['challenges'])}
            self.contest_history['contests'].append(contest)
            json.dump(self.contest_history, open('cogs/contestcog/contesthistory.json', 'w'), indent = 2)

            for channel in channels:
                await channel.delete_messages(await channel.history(limit = None).flatten())
                await channel.send(f"**Entertain me, mortals.** {contest['challenge']} you can in this channel!\n"
                                   f"Vote on your favorite with {self.bot.get_emoji(509383247772385311)}. The most "
                                   f"votes before Sunday wins!\n"
                                   "Post only once, I don't want to have to delete messages. Same goes for votes.")

        # Tally up contest results and announce winner.
        elif datetime.datetime.today().weekday() == 6:
            for channel in channels:
                tally = {}
                for message in await channel.history().flatten():
                    if not message.author.bot:
                        tally[str(message.author.id)] = [react.count if react.emoji.id == 509383247772385311
                                                         else 0 for react in message.reactions][0]
                        print(tally)
                winners = [key for key in tally.keys() if tally[key] == max(tally.values())]

                if len(winners) == 0:
                    response = "No winners this week."
                elif len(winners) > 1:
                    response = f"{', '.join([self.bot.get_user(int(user_id)) for user_id in winners][:-1])} and" \
                               f" {[self.bot.get_user(int(user_id)) for user_id in winners][-1]} won!"
                else:
                    response = f"{self.bot.get_user(int(winners[0]))} won!"

                await channel.delete_messages(await channel.history(limit = None).flatten())
                await channel.send(response)
        print("Contest checked.")


def setup(bot):
    bot.add_cog(ContestCog(bot))
