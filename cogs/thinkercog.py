from discord.ext import commands
import discord
from datetime import date, timedelta
import random
from random import randrange
import requests
import nltk


class ThinkerCog:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def random_date(start, end):
        """Return a random datetime between two datetime objects."""
        return start + timedelta(days = randrange((end - start).days))

    @commands.command()
    async def apod(self, ctx, focus: str = date.today().strftime("%y%m%d")):
        """
        Sends a photo from NASA's APotD.

        Usage:
            apod <date>
            apod random
        """
        embed = discord.Embed(title = "Command: apod", color = 0x0000FF)
        if focus.lower() == "random":
            day = self.random_date(date(1995, 6, 1), date.today()).strftime("%y%m%d")
        else:
            day = focus.strip("/")

        pic_source = requests.get(f'https://apod.nasa.gov/apod/ap{day}.html').text  # Gets source code for the apod site

        if '<IMG SRC=' in pic_source:
            image_spot = pic_source.find('<IMG SRC=') + 10  # Finds image location
            image_spot_end = pic_source[image_spot:].find('"') + image_spot  # Finds end of image url
            embed.description = day
            embed.set_image(url = f"https://apod.nasa.gov/apod/{pic_source[image_spot:image_spot_end]}")
        elif '<iframe ' in pic_source:
            vid_spot = pic_source.find('<iframe ') + 68
            vid_spot_end = pic_source[vid_spot:].find('?rel') + vid_spot
            embed.description = day
            embed.set_image(url = f"https://www.youtube.com/watch?v={pic_source[vid_spot:vid_spot_end]}")
        else:
            embed.description = "NASA was stupid on this day and decided to use a flash player trash. Try again, buddy."
            embed.color = 0xFF0000

        await ctx.send(embed = embed)

    @commands.command()
    async def answer(self, ctx):
        embed = discord.Embed(title = "Command: answer", color = 0x0000FF, description = ctx.message.content)
        questions = ctx.message.content.split(' or ')
        for chunk in questions:
            for word, tag in nltk.pos_tag(nltk.tokenize.word_tokenize(chunk), tagset = 'universal'):
                if tag == 'PRON' or word == 'should' or word == '?':
                    chunk.remove(word)
        if len(questions) == 1:
            embed.set_footer(text = random.choice(["yes", "yas", "yep", "yup", "no", "nop", "nope", "noperino"]))
        else:
            embed.set_footer(text = random.choice(questions))
        ctx.send(embed = embed)

    @commands.command(name = "xkcd")
    async def fetch_xkcd(self, ctx, number: int = 0):
        embed = discord.Embed(title = "Command: XKCD")
        if number == 0:
            comic_source = requests.get("https://c.xkcd.com/random/comic/")
        else:



def setup(bot):
    bot.add_cog(ThinkerCog(bot))
