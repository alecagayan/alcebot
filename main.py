import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import platform
import sys
import os
import random
import requests
import urllib.request
import json
import time
import pyowm
import datetime
now = datetime.datetime.now()
diff = datetime.datetime(now.year, 12, 25) - \
    datetime.datetime.today()  # Days until Christmas
passcode = str(random.randint(10000000000000000000,99999999999999999999))
owm = pyowm.OWM('edfb0cd2f5f17a2319a2bdc8b94431cd')


import logging
from pyfiglet import figlet_format, FontNotFound


# Config.py setup
##################################################################################
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")

else:
    import config  # config.py is required to run; found in the same directory.
    from setup import ver # setup.py is used to get the version number
##################################################################################


# This code logs all events including chat to discord.log. This file will be overwritten when the bot is restarted - rename the file if you want to keep it.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=config.logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# IMPORTANT - DO NOT TOUCH! Setup bot as "client", with description and prefix from config.py
client = Bot(description=config.des, command_prefix=config.pref)


# This message lets us know that the script is running correctly
print("Connecting...")


# Start bot and print status to console
@client.event
async def on_ready():
    print("Bot online!\n")
    print("Discord.py API version:", discord.__version__)
    print("Python version:", platform.python_version())
    print("Running on:", platform.system(), platform.release(), "(" + os.name + ")")
    print("BlazeBot version:", ver)
    print("Name : {}".format(client.user.name))
    print("Client ID : {}".format(client.user.id))
    print("Currently active on " + str(len(client.guilds)) + " server(s).\n")
    logger.info("Bot started successfully.")

    await client.change_presence(status=discord.Status.online, activity=discord.Game('a!'))

    # Set "playing" status
    if diff.days < 2:
        print("Merry Christmas!")
        game = "Merry Christmas! <3"
    else:
        game = "BlazeBot.py | {0}help | Python version: {1} | Discord API version: {2} | Running on: {3} {4} ({5})".format(config.pref, platform.python_version(), discord.__version__, platform.platform, platform.release(), os.name)
        
    await client.change_presence(status=discord.Status.online, activity=discord.Game('a!'))


# Default BlazeBot commands

#add
@client.command()
async def add(ctx, a: float, b: float):
    await ctx.send(a+b)

#subtract
@client.command()
async def subtract(ctx, a: float, b: float):
    await ctx.send(a-b)

@client.command()
async def multiply(ctx, a: float, b: float):
    await ctx.send(a*b)

#divide
@client.command()
async def divide(ctx, a: float, b: float):
    await ctx.send(a/b)

#exponent
@client.command()
async def power(ctx, a: float, b: float):
    await ctx.send(a**b)

#tells you to die
@client.command()
async def cleck(ctx):
    await ctx.send("https://imagen.click/i/7cd655.png")

@client.command()
async def github(ctx):
    await ctx.send("https://github.com/oopsie1412/alcebot")

#prints invite
@client.command()
async def invite(ctx):
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=480451439181955093&scope=bot&permissions=8")

#roll a die
@client.command()
async def roll(ctx):
    await ctx.send(config.die_url[random.randint(1,6)-1])

@client.command()
async def pasta(ctx):
    await ctx.send('cut em thiccque daddy')

#translate
@client.command()
async def credit(ctx):
    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="Thanks to these people:", color=embedColor)

    embed.add_field(name="Author", value='oopsie#1412')
    embed.add_field(name="GitHub Contributors", value='lincoln-bridge, gidoBOSSftw5731')
    embed.add_field(name="Discord Contributors", value='Motions#5324, GidoBOSSftw5731#6422, chickenramen#7173')
    embed.add_field(name="Beta Testers", value='oopsie#1412')


    await ctx.send(embed=embed)

#sentiment
@client.command()
async def netdiskcpu(ctx, a):
    if(passcode == a):

        await ctx.channel.purge(limit=1)
        embedColor = random.randint(0, 0xffffff)
        embed = discord.Embed(title="Stats:", color=embedColor)

        embed.add_field(name="Net IO Counters", value=psutil.net_io_counters())
        embed.add_field(name="Disk IO Counters", value=psutil.disk_io_counters())
        embed.add_field(name="Disk Usage", value=psutil.disk_usage('/'))
        embed.add_field(name="CPU Stats", value=psutil.cpu_stats())
        embed.add_field(name="CPU Times", value=psutil.cpu_times())

        await ctx.send(embed=embed)
    else:
        await ctx.send('Incorrect administrator passcode!')

#sentiment
@client.command()
async def hugeveryone(ctx):
    await ctx.send("@here has been hugged by " + ctx.message.author.mention + "!")

@client.command()
async def suggest(ctx, *, a):
    await ctx.send("Thank you for the suggestion! I will get back to you soon!")
    print ("suggestion: " + a)

@client.command()
async def belsontrump(ctx):
    await ctx.send("https://imagen.click/i/b8626b.jpg")
    await ctx.send("https://imagen.click/i/846a0e.jpg")

@client.command()
async def weather(ctx, a):

    wheathr1 = ''
    wheathr2 = ''
    wheathr3 = ''
    wheathr4 = ''
    wheathr5 = ''
    wheathr6 = ''

    wethr = owm.weather_at_zip_code(a,'US')
    weather = wethr.get_weather()
    la = owm.three_hours_forecast(a + ', US')
    j = wethr.get_location()
    k = str(j.get_name())

#    if (la.will_have_storm()):
#        wheathr1 = ':thunder_cloud_rain:'
#    if (la.will_have_snow()):
#        wheathr2 = ':snowflake:'
#    if (la.will_have_fog()):
#        wheathr3 = ':fogblob:'
#    if (la.will_have_clouds()):
#        wheathr4 = ':cloud:'
#    if (la.will_have_clear()):
#        wheathr6 = ':sunny:'

    embedColor = random.randint(0, 0xffffff)

    status = weather.get_detailed_status()

    embed = discord.Embed(title="Weather in " + k + " right now:", color=embedColor) #embed title with zip
    embed.add_field(name="Temperature :thermometer:", value=str(weather.get_temperature('celsius')['temp']) + ' C', inline=False) #temperature
    embed.add_field(name="Conditions :white_sun_rain_cloud:", value=status, inline=False) #conditions header with emoji conditions
    embed.add_field(name="Wind :wind_blowing_face:", value=str(round(weather.get_wind('miles_hour')['speed'], 1)) + ' mph', inline=False) #wind speed
    embed.add_field(name="Humidity :droplet:", value=str(weather.get_humidity()) + '%', inline=False) #humidity
    embed.add_field(name="Visibility :eye:", value=str(round(weather.get_visibility_distance()/1609.344, 1)) + ' miles', inline=False) #visibility
    embed.set_footer(text='Requested on ' + str(time.ctime())) #prints time

    await ctx.send(embed=embed)

@client.command()
async def info(ctx): 

    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="alcebot", description="worst bot lol", color=embedColor)

    # give info about you here
    embed.add_field(name="Author", value="oopsie#1412")
    embed.add_field(name="Users", value=len(ctx.bot.users), inline=False)
    embed.add_field(name="Commands", value=len(ctx.bot.commands), inline=False)
    embed.add_field(name="Processes", value='CPU Usage: ' + str(psutil.cpu_percent()) + "% ", inline=False)
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=480451439181955093&scope=bot&permissions=8)")
    embed.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed.set_footer(text='Requested on ' + str(time.ctime())) #prints time

    await ctx.send(embed=embed)

client.remove_command('help')

 #adds help command with embed. embed for big brain
@client.command()
async def help(ctx):
    embedColor = random.randint(0, 0xffffff)

    embed = discord.Embed(title="alcebot", description="horrible bot = horrible commands. List of commands are:", color=embedColor)
    embed.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed.add_field(name="a!info", value="Gives a little info about the bot.", inline=False)
    embed.add_field(name="a!add <x y>", value="Gives the sum of **X** and **Y**.", inline=False)
    embed.add_field(name="a!subtract <x y>", value="Gives the difference of **X** and **Y**.", inline=False)
    embed.add_field(name="a!multiply <x y>", value="Gives the product of **X** and **Y**.", inline=False)
    embed.add_field(name="a!divide <x y>", value="Gives the quotient of **X** and **Y**.", inline=False)
    embed.add_field(name="a!power <x y>", value="Gives **X** to the **Y** power.", inline=False)
    embed.add_field(name="a!greet", value="Gives a nice greet message.", inline=False)
    embed.add_field(name="a!die", value="Gives a dead body dragging across the floor.", inline=False)
    embed.add_field(name="a!roll", value="Roll a random number from 1 to 6.", inline=False)
    embed.add_field(name="a!translate <x y>", value="Gives translation with **X** as abbreviated language and **Y** as 1 word", inline=False)
    embed.add_field(name="a!sentiment <sentence>", value="Shows sentiment and polarity of the sentence", inline=False)
    embed.add_field(name="a!weather <zipcode>", value="Gives the latest weather in the area", inline=False)
    embed.add_field(name="a!compliment <x>", value='"Compliments" the tagged user. If nobody is tagged, prints a random compliment', inline=False)
    embed.add_field(name="a!help", value="Gives this message. HEEEEEELP!", inline=False)
    embed.set_footer(text='Requested on ' + str(time.ctime())) #prints time
    
    await ctx.send(embed=embed)

@client.command(aliases=['remove', 'delete'])
async def purge(ctx, number: int):
    """Bulk-deletes messages from the channel."""
    try:
        if ctx.message.author.guild_permissions.administrator:
        
            deleted = await ctx.channel.purge(limit=number)
            print('Deleted {} message(s)'.format(len(deleted)))
            logger.info('Deleted {} message(s)'.format(len(deleted)))

        else:
            await ctx.send(config.err_mesg_permission)
    except:
        await ctx.send(config.err_mesg_generic)


@client.command()
async def roles(context):
    """Lists the current roles on the server."""

    roles = context.message.guild.roles
    result = "**The roles on this server are: **"
    for role in roles:
        result += role.name + ", "
    await ctx.send(result)


@client.command()
async def hug(ctx, *, member: discord.Member = None):
    """Hug someone on the server <3"""
    try:
        if member is None:
            await ctx.send(ctx.message.author.mention + " has been hugged!")
        else:
            if member.id == ctx.message.author.id:
                await ctx.send(ctx.message.author.mention + " has hugged themself!")
            else:
                await ctx.send(member.mention + " has been hugged by " + ctx.message.author.mention + "!")

    except:
        await ctx.send(config.err_mesg_generic)


@client.command(aliases=['say'])
async def echo(ctx, *msg):
    """Makes the bot talk."""
    try:
        say = ' '.join(msg)
        await client.delete_message(ctx.message)
        return await ctx.send(say)
    except:
        await ctx.send(config.err_mesg_generic)


@client.command(aliases=['saytts'])
async def echotts(ctx, *msg):
    """Makes the bot talk, with TTS."""
    try:
        say = ' '.join(msg)
        await client.delete_message(ctx.message)
        return await ctx.send(say, tts=True)
    except:
        await ctx.send(config.err_mesg_generic)


@client.command(aliases=["fancy"])
async def fancify(ctx, *, text):
    """Makes text fancy!"""
    try:
        def strip_non_ascii(string):
            """Returns the string without non ASCII characters."""
            stripped = (c for c in string if 0 < ord(c) < 127)
            return ''.join(stripped)

        text = strip_non_ascii(text)
        if len(text.strip()) < 1:
            return await self.ctx.send(":x: ASCII characters only please!")
        output = ""
        for letter in text:
            if 65 <= ord(letter) <= 90:
                output += chr(ord(letter) + 119951)
            elif 97 <= ord(letter) <= 122:
                output += chr(ord(letter) + 119919)
            elif letter == " ":
                output += " "
        await ctx.send(output)

    except:
        await ctx.send(config.err_mesg_generic)


@client.command()
async def bigtext(ctx, *, text):
    """Enlarges text."""
    try:
        await ctx.send("```fix\n" + figlet_format(text, font="big") + "```")
    except:
        await ctx.send(config.err_mesg_generic)


@client.command(aliases=['game', 'presence'])
async def setgame(ctx, *args):
    """Sets the 'Playing' status."""
    try:
        if ctx.message.author.guild_permissions.administrator:
            setgame = ' '.join(args)
            await client.change_presence(status=discord.Status.online, activity=discord.Game(setgame))
            await ctx.send(":ballot_box_with_check: Game name set to: `" + setgame + "`")
            print("Game set to: `" + setgame + "`")
        else:
            await ctx.send(config.err_mesg_permission)
    except:
        await ctx.send(config.err_mesg_generic)


@client.command()
async def botplatform(ctx):
    """Shows what OS the bot is running on."""
    try:
        await ctx.send("The bot is currently running on: ```" + str(platform.platform()) + "```")
    except:
        await ctx.send(config.err_mesg_generic)



@client.command()
async def serverlist(ctx):
    """List the servers that the bot is active on."""
    x = ', '.join([str(server) for server in client.guilds])
    y = len(client.guilds)
    print("Server list: " + x)
    if y > 40:
        embed = discord.Embed(title="Currently active on " + str(y) + " servers:", description=config.err_mesg_generic + "```json\nCan't display more than 40 servers!```", colour=0xFFFFF)
        return await ctx.send(embed=embed)
    elif y < 40:
        embed = discord.Embed(title="Currently active on " + str(y) + " servers:", description="```json\n" + x + "```", colour=0xFFFFF)
        return await ctx.send(embed=embed)


@client.command()
async def getbans(ctx):
	"""Lists all banned users on the current server."""
	
	if ctx.message.author.guild_permissions.ban_members:
		x = await ctx.message.guild.bans()
		x = '\n'.join([str(y.user) for y in x])
		embed = discord.Embed(title="List of Banned Members", description=x, colour=0xFFFFF)
		return await ctx.send(embed=embed)
	else:
		await ctx.send(config.err_mesg_permission)
	



@client.command(aliases=['user'])
async def userinfo(ctx, user: discord.Member):
	"""Gets info on a member, such as their ID."""
	try:
		embed = discord.Embed(title="User profile: " + user.name, colour=user.colour)
		embed.add_field(name="Name:", value=user.name)
		embed.add_field(name="ID:", value=user.id)
		embed.add_field(name="Status:", value=user.status)
		embed.add_field(name="Highest role:", value=user.top_role)
		embed.add_field(name="Joined:", value=user.joined_at)
		embed.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=embed)
	except:
		await ctx.send(config.err_mesg_generic)



@client.command()
async def ping(ctx):
    print(client.latency)
    await ctx.send('Pong! {0}ms websocket latency'.format(round(client.latency*1000, 3)))

# Choose a random insult from the list in config.py
@client.command()
async def insult(ctx):
    """Says something mean about you."""
    await ctx.send(ctx.message.author.mention + " " + random.choice(config.insults))  # Mention the user and say the insult

@client.command()
async def load(ctx):
    """Loads startup extensions."""
    if __name__ == "__main__":  # Load startup extensions, specified in config.py
        for extension in config.startup_extensions:
            try:
                client.load_extension(extension)
                print("Loaded extension '{0}'".format(extension))
                logger.info("Loaded extension '{0}'".format(extension))
            except Exception as e:
                exc = '{0}: {1}'.format(type(e).__name__, e)
                print('Failed to load extension {0}\nError: {1}'.format(extension, exc))
                logger.info('Failed to load extension {0}\nError: {1}'.format(extension, exc))

# Christmas countdown!
@client.command(aliases=['xmas', 'chrimbo'])
async def christmas(ctx):
    """Christmas countdown!"""
    await ctx.send("**{0}** day(s) left until Christmas day! :christmas_tree:".format(str(diff.days)))  # Convert the 'diff' integer into a string and say the message


if __name__ == "__main__":  # Load startup extensions, specified in config.py

    if not config.startup_extensions:
        print("No extensions enabled.")
    else:
        print("Loading extensions...")

    for extension in config.startup_extensions:
        try:
            client.load_extension(extension)
            print("Loaded extension '{0}'".format(extension))
            logger.info("Loaded extension '{0}'".format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\nError: {}'.format(extension, exc))
            logger.info('Failed to load extension {}\nError: {}'.format(extension, exc))



if __name__ == "__main__":

    # Read client token from "config.py" (which should be in the same directory as this file)
    client.run(config.bbtoken)
