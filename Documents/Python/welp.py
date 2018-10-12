import discord
import random
import requests
from discord.ext.commands import Bot
from datetime import date

Bot_Prefix = ("?", "!")

client = Bot(command_prefix=Bot_Prefix)

@client.event
async def on_ready():
    print ('I have logged in as {0.user}'.format(client))
    await client.send_message(discord.Object(id='280183677697392641'), 'I am ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'I am here {0.author.mention}'.format(message))
    
    if message.content.startswith('!a'): #Begins "answer" command
        if message.content.startswith('!a help'):
            await client.send_message(message.channel, "I will give you an answer! Make sure to include all your words or else I will sound dumb. If you don't give me some context, I'll give you a simple answer like:")
        
        t = message.content #Just an abbreviation
        lt = t.lower() #Basically searches for capitalized & not words
        option1 = '1'
        option2 = '2'
        if ' or ' in t: #Checks if user is asking btwn 2 options
            start = 3
            end = 0
            half = t.find(' or ') #Finds the point between the 2 options
        
            if ' should ' in lt: #Checks if "should" is being asked
                if ' i ' in lt: #Checking for 1 letter pronouns
                    start = lt.find(' i ') + 3
                if ' he ' in lt: #Checking for 2 letter pronouns
                    start = lt.find(' he ') + 4
                if ' we ' in lt: #Checking for 2 letter pronouns
                    start = lt.find(' we ') + 4
                if ' it ' in lt: #Checking for 2 letter pronouns
                    start = lt.find(' it ') + 4
                if ' you ' in lt: #Checking for 3 letter pronouns
                    start = lt.find(' you ') + 5
                if ' she ' in lt: #Checking for 3 letter pronouns
                    start = lt.find(' she ') + 5
                if ' they ' in lt: #Checking for 4 letter pronouns
                    start = lt.find(' they ') + 6
                if " y'all " in lt: #Checking for 4 letter pronouns
                    start = lt.find(" y'all ") + 7
        
            if ' or ' in t[half + 3:]:
                nextPart = t[half + 4:]
                options = [t[start:half], nextPart[:nextPart.find(' or ')]]
                while ' or' in nextPart[4:]:
                    nextPart = nextPart[nextPart.find(' or ') + 4:]
                    nextEnd = nextPart.find(' or ')
                    options.append(nextPart[:nextEnd])
                if not t.endswith('?'):
                    options[-1] = options[-1] + t[-1]
                await client.send_message(message.channel, random.choice(options) + ' ')
            
            else:
                option1 = t[start:half] #Generates the first option proposed
                option2 = t[half + 4:] #Generates the second option proposed
                if '?' in t:
                    option2 = t[half + 4:-1] #Generates the second option proposed
                await client.send_message(message.channel, random.choice([option1, option2]) + ' ')
        else:
            await client.send_message(message.channel, random.choice(["yes", "yas", "yep", "yup", "no", "nop", "nope", "noperino"]))

    if message.content.startswith('apod'):
        today = str(date.today())
        day = message.content[7:9] + message.content[10:12] + message.content[13:15]
        if message.content.endswith('apod'):
            day = today[2:4] + today[5:7] + today[8:10]
        if message.content.endswith('random'):
            year = random.randint(1995, int(today[0:4]))
            
            month = random.randint(1, 12)
            if year == 1995:
                month = random.randint(6, 12)
            if year == 2018:
                month = random.randint(1, int(today[5:7]))
            
            daym = random.randint(1, 31)
            if month == 2:
                daym = random.randint(1, 28)
                if month % 4 == 0:
                    daym = random.randint(1, 29)
            if month == 4 or month == 6 or month == 9 or month == 11:
                daym = random.randint(1, 30)
            
            if month < 10:
                month = '0' + str(month)
            if daym < 10:
                daym = '0' + str(daym)
            
            day = str(year)[2:4] + str(month) + str(daym)
        
        pic_source = requests.get('https://apod.nasa.gov/apod/ap' + day + '.html').text #Gets the source code for the apod site
        image_spot = pic_source.find('<IMG SRC=') + 10 #Finds wherever the image is
        image_spot_end = pic_source[image_spot:].find('"') + image_spot #Finds the end of the image url
        image_url = 'https://apod.nasa.gov/apod/' + pic_source[image_spot:image_spot_end] #Constructs the actual image url
        if '<IMG SRC=' in pic_source:
            await client.send_message(message.channel, day + '  ' + image_url)
        elif '<iframe ' in pic_source:
            vid_spot = pic_source.find('<iframe ') + 68
            vid_spot_end = pic_source[vid_spot:].find('?rel') + vid_spot
            vid_url = 'https://www.youtube.com/watch?v=' + pic_source[vid_spot:vid_spot_end]
            await client.send_message(message.channel, day + "  " + vid_url)
        else:
            client.send_message(message.channel, 'Nasa was stupid on this day, and decided to use some flash player trash. Try again, buddy.')
    
client.run('NDkzMTAyNzEzNzEwNTc1NjE2.DogxgA.z2h-R8kHg4hlOHbFDIybU-KSiH0')
