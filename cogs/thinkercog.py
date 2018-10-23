from discord.ext import commands
import discord
from datetime import date, timedelta
import random
from random import randrange
import requests
import nltk
from bs4 import BeautifulSoup
import re


class ThinkerCog:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def random_date(start, end):
        """Return a random datetime between two datetime objects."""
        return start + timedelta(days = randrange((end - start).days))

    @commands.command()
    async def apod(self, ctx, focus: str = date.today().strftime("%y%m%d")):
        """Sends a photo from NASA's APotD."""
        embed = discord.Embed(title = "Command: apod", color = 0x0000FF)
        if focus.lower() == "random":
            day = self.random_date(date(1995, 6, 1), date.today()).strftime("%y%m%d")
        else:
            day = focus.strip('/')

        pic_source = requests.get(f"https://apod.nasa.gov/apod/ap{day}.html").text

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
    async def answer(self, ctx, *question: str):
        """Answers a basic question."""
        embed = discord.Embed(title = "Command: answer", color = 0x0000FF,
                              description = " ".join(*question))
        questions = " ".join(*question).strip('?').split(' or ')
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

    @commands.command(name = "xkcd")
    async def fetch_xkcd(self, ctx, number: int = 0):
        """Fetches an XKCD comic."""
        embed = discord.Embed(title = "Command: XKCD", color = 0x0000FF)
        if number == 0:
            soup = BeautifulSoup(requests.get('https://c.xkcd.com/random/comic/').text, 'html.parser')
        else:
            if requests.get(f'https://xkcd.com/{number}/').status_code != 404:
                soup = BeautifulSoup(requests.get(f'https://xkcd.com/{number}/').text, 'html.parser')
            else:
                soup = BeautifulSoup(requests.get('https://xkcd.com/').text, 'html.parser')
                embed.set_footer(text = "The requested comic is unavailable. Have this one instead.")
        embed.set_image(url = f"https:{soup.find('div', id = 'comic').img['src']}")
        embed.description = f"**{soup.find(text = re.compile('Permanent link to this comic:'))[48:-1]} "\
                            f": {soup.find('div', id = 'comic').img['alt']}**"
        embed.set_footer(text = f"{soup.find('div', id = 'comic').img['title']}")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['ud'])
    async def urban(self, ctx, *search):
        """Searches on the Urban Dictionary."""
        try:
            # Send request to the Urban Dictionary API and grab info
            response = requests.get("http://api.urbandictionary.com/v0/define",
                                    params = [("term", ' '.join(search))]).json()
            embed = discord.Embed(description = "No results found!", color = 0xFF0000)
            if len(response["list"]) == 0:
                return await ctx.send(embed = embed)
            # Add results to the embed
            embed = discord.Embed(title = "Word", description = ' '.join(search), color = 0x0000FF)
            embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
            embed.add_field(name = "Examples:", value = response['list'][0]["example"])
            embed.set_footer(text = f"Tags: {', '.join(response['tags'])}")
            await ctx.send(embed = embed)

        except:
            await ctx.send("It done messed up.")


def setup(bot):
    bot.add_cog(ThinkerCog(bot))
