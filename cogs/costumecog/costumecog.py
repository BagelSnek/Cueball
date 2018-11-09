import os
import datetime
import discord
import aiocron


class CostumeCog(discord.Client):
    """CostumeCog is a cog that automagically changes the profile picture of Cueball for the holiday.
    Costumes must be .png files, named as **startdate-picturename-enddate.png**"""
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.bg_task = self.loop.create_task(self.check_costume())
        self._update_cron = aiocron.crontab('1 0 * * *', func = self.check_costume, start = True)

    async def check_costume(self):
        await self.bot.wait_until_ready()
        picture = open('cogs/costumecog/standard.png', 'rb')
        for file in [f.strip('.png').split('-') for f in os.listdir('cogs/costumecog/costumes/')
                     if os.path.isfile(os.path.join('cogs/costumecog/costumes/', f))]:
            if int(file[0]) <= int(datetime.date.today().strftime("%m%d")) <= int(file[2]):
                picture = open(f'cogs/costumecog/costumes/{"-".join(file)}.png', 'rb')

        await self.bot.user.edit(avatar = picture.read())
        print("Costume checked.")


def setup(bot):
    bot.add_cog(CostumeCog(bot))
