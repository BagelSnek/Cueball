import asyncio
import os
import datetime
import aiocron
from cogs.utils.dataIO import dataIO


class CostumeCog:
    """
    CostumeCog is a cog that automagically changes the profile picture of Cueball for the holiday.
    Costumes must be .png files, named as **startdate-picturename-enddate.png**
    -- Designed for use with Cueball --
    """
    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.check_costume())
        self._update_cron = aiocron.crontab('1 0 * * *', func = self.check_costume, start = True)

    async def check_costume(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(3)
        print("Checking costume...")

        picture = open(os.path.join(dataIO.path, 'costumes', 'standard.png'), mode = 'rb')
        for file in [f.strip('.png').split('-') for f in os.listdir('data/costumes')
                     if os.path.isfile(os.path.join('data/costumes', f))]:
            if int(file[0]) <= int(datetime.date.today().strftime("%m%d")) <= int(file[2]):
                picture = open(os.path.join(dataIO.path, 'costumes', f'{"-".join(file)}.png'), mode = 'rb')
                break

        await self.bot.user.edit(avatar = picture.read())
        print("Costume checked.\n")


def setup(bot):
    bot.add_cog(CostumeCog(bot))
