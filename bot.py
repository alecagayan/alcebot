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
import config
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import urllib
import urllib.request

import psutil
import aiohttp
from concurrent.futures._base import CancelledError
import glob

now = datetime.datetime.now()
start_time = time.time()
diff_cmas = datetime.datetime(now.year, 12, 25) - \
datetime.datetime.today()
diff_ny = datetime.datetime(now.year + 1, 1, 1) - \
datetime.datetime.today()  # Days until Christmas
passcode = str(random.randint(10000000000000000000,99999999999999999999))
devID = 401063536618373121
owm = pyowm.OWM(config.owm_key)
filename_state = "/opt/alcebot/alcebot/states.csv"
filename_county = "/opt/alcebot/alcebot/counties.csv"
county_graph = '/opt/alcebot/alcebot/plot-county.png'
state_graph = '/opt/alcebot/alcebot/plot-state.png'
#translate = Translator()

import logging
# This code logs all events including chat to discord.log. This file will be overwritten when the bot is restarted - rename the file if you want to keep it.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=config.logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or('a!')(client, message)
    with open('prefixes.json', 'r') as f:
        prefixes=json.load(f)
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or('a!')(client, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(client, message)

def file_age_in_seconds(pathname):
    st = os.stat(pathname)
    return (time.time() - st.st_mtime)


# IMPORTANT - DO NOT TOUCH! Setup bot as "client", with description and prefix from config.py
client = Bot(description=config.des, command_prefix=get_prefix)

#load cogs
client.load_extension("cogs.prefix")
client.load_extension("cogs.random")
client.load_extension("cogs.mod")
client.load_extension("cogs.music")
client.load_extension("cogs.poll")
client.load_extension("cogs.info")


# This message lets us know that the script is running correctly
print("Connecting...")

# Start bot and print status to console
@client.event
async def on_ready():
    print("Bot online!\n")
    print("Discord.py API version:", discord.__version__)
    print("Python version:", platform.python_version())
    print("Running on:", platform.system(), platform.release(), "(" + os.name + ")")
    print("Name : {}".format(client.user.name))
    print("Client ID : {}".format(client.user.id))
    print("Currently active on " + str(len(client.guilds)) + " server(s).\n")
    logger.info("Bot started successfully.")

    await client.change_presence(status=discord.Status.online, activity=discord.Game('a!'))

    # Set "playing" status
    if diff_cmas.days < 2:
        print("Merry Christmas!")
        game = "Merry Christmas! <3"
    else:
        game = "a!"
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game))

#@client.event
#async def on_member_join(member):
#    if(guild.id == )
#    role = discord.utils.get(member.server.roles, id="<role ID>")
#    await client.add_roles(member, role)

@client.command()
async def whattimeisit(ctx):
    await ctx.send(time.ctime())

@client.command()
async def _joinvc(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

#math
@client.command()
async def math(ctx, m, a: float, b: float):
    if(m == 'add'):
        await ctx.send(a+b)
    elif(m == 'subtract'):
        await ctx.send(a-b)
    elif(m == 'multiply'):
        await ctx.send(a*b)
    elif(m == 'divide'):
        await ctx.send(a/b)
    elif(m == 'power'):
        await ctx.send(a**b)
    elif(m == 'exponent'):
        await ctx.send(a**b)

@client.command()
async def covid(ctx, type, *, state):


    
    if(type == "state"):

        if (not os.path.exists(filename_state) or file_age_in_seconds(filename_state) > 3600):
            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", filename_state)

        df = pd.read_csv(filename_state)
        df_state = df[ df['state'] == state ]
        df_state.plot(x='date', y=['cases', 'deaths'], label=['Cases', 'Deaths'], linestyle='-', linewidth=4)
        plt.savefig(state_graph)
        await ctx.send(file=discord.File(state_graph))


    if(type == "county"):

        if (not os.path.exists(filename_county) or file_age_in_seconds(filename_county) > 3600):
            urllib.request.urlretrieve("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv", filename_county)
        df = pd.read_csv(filename_county)
        df_county = df[ df['county'] == state ]
        df_county.plot(x='date', y=['cases', 'deaths'], label=['Cases', 'Deaths'], linestyle='-', linewidth=4)
        plt.savefig(county_graph)
        await ctx.send(file=discord.File(county_graph))


#shows ms cleckley !
@client.command()
async def cleck(ctx):
    await ctx.send("https://imagen.click/i/7cd655.png")

#sends github link
@client.command()
async def github(ctx):
    await ctx.send("https://github.com/oopsie1412/alcebot/tree/beta")

#prints invite
@client.command()
async def invite(ctx):
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=633431761094705163&scope=bot&permissions=8")

#roll a die
@client.command()
async def roll(ctx):
    await ctx.send(config.die_url[random.randint(1,6)-1])

#sends a compliment from compliment list in config.py
@client.command()
async def compliment(ctx):
    await ctx.send(config.compliments[random.randint(0,14)])

@commands.command()
async def die(ctx):
    if(ctx.author.id == 401063536618373121):
        await ctx.send("Drinking bleach.....")
        await ctx.logout()
    else:
        await ctx.send(config.err_mesg_permission)

@commands.command()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=ctx.message.author.top_role.colour)
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text='Requested on ' + str(time.ctime()))

    await ctx.send(embed=embed)

#you'll find out soon enough
@client.command()
async def pasta(ctx):
    await ctx.send('cut em thiccque daddy')

#random xkcd comic
@client.command()
async def xkcd(ctx,  *searchterm: str):

        apiUrl = 'https://xkcd.com{}info.0.json'
        async with aiohttp.ClientSession() as cs:
            async with cs.get(apiUrl.format('/')) as r:
                js = await r.json()
                if ''.join(searchterm) == 'random':

                    randomComic = random.randint(0, js['num'])
                    async with cs.get(apiUrl.format('/' + str(randomComic) + '/')) as r:
                        if r.status == 200:
                            js = await r.json()
                comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
                date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
                msg = '**{}**\n{}\nXKCD Link: <{}> ({})'.format(js['safe_title'], js['img'], comicUrl, date)
                await ctx.send(msg)

#shows current info on server		
@client.command(pass_context=True, aliases=['serverinfo', 'guild', 'membercount'])
async def server(ctx):

    #prints server info
    roles = ctx.guild.roles
    embed = discord.Embed(color=0xf1c40f) #Golden
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text='Requested on ' + str(time.ctime()))
    embed.add_field(name='Name', value=ctx.guild.name, inline=True)
    embed.add_field(name='ID', value=ctx.guild.id, inline=True)
    embed.add_field(name='Owner', value=ctx.guild.owner, inline=True)
    embed.add_field(name='Region', value=ctx.guild.region, inline=True)
    embed.add_field(name='Member Count', value=ctx.guild.member_count, inline=True)
    embed.add_field(name='Creation', value=ctx.guild.created_at.strftime('%d.%m.%Y'), inline=True)
    embed.set_footer(text='Requested on ' + str(time.ctime()))

    await ctx.send(embed=embed)

#credits contributors
@client.command()
async def credit(ctx):
    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="Thanks to these people:", color=embedColor)

    embed.add_field(name="Author", value='oopsie#1412')
    embed.add_field(name="GitHub Contributors", value='lincoln-bridge, gidoBOSSftw5731, iCrazyBlaze, rgb4')
    embed.add_field(name="Discord Contributors", value='always#5324, GidoBOSSftw5731#6422, chickenramen#7173')
    embed.add_field(name="Beta Testers", value='oopsie#1412')
    embed.set_footer(text='Requested on ' + str(time.ctime()))

    await ctx.send(embed=embed)

#displays premium info
@client.command()
async def premium(ctx):
    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="AlceBot Premium", color=embedColor)

    embed.add_field(name="Get Premium", value='You already have premium, silly!')
  
    await ctx.send(embed=embed)

#sentiment
@client.command()
async def netdiskcpu(ctx):
    if(ctx.author.id == 401063536618373121):
        await ctx.channel.purge(limit=1)
        embedColor = random.randint(0, 0xffffff)
        embed = discord.Embed(title="Stats:", color=embedColor)

        embed.add_field(name="Net IO Counters", value=psutil.net_io_counters())
        embed.add_field(name="Disk IO Counters", value=psutil.disk_io_counters())
        embed.add_field(name="Disk Usage", value=psutil.disk_usage('/'))
        embed.add_field(name="CPU Stats", value=psutil.cpu_stats())
        embed.add_field(name="CPU Times", value=psutil.cpu_times())
        embed.set_footer(text='Requested on ' + str(time.ctime()))

        await ctx.send(embed=embed)
    else:
        await ctx.send(config.err_mesg_permission)

#hugs everyone
@client.command()
async def hugeveryone(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("@here has been hugged by " + ctx.message.author.mention + "!")
    await ctx.send("https://gph.is/g/ajxG084")

#marks a suggestion in log
@client.command()
async def suggestion(ctx, *, a):
    await ctx.send("Thank you for the suggestion! I will get back to you soon!")
    print ("suggestion: " + a)

#BELSON AND TRUMP ARE THE SAME
@client.command()
async def belsontrump(ctx):
    await ctx.send("https://imagen.click/i/b8626b.jpg")
    await ctx.send("https://imagen.click/i/846a0e.jpg")

#Shows the current weather at zip code	
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

    if (la.will_have_storm()):
        wheathr1 = ':thunder_cloud_rain:'
    if (la.will_have_snow()):
        wheathr2 = ':snowflake:'
    if (la.will_have_fog()):
        wheathr3 = ':fogblob:'
    if (la.will_have_clouds()):
        wheathr4 = ':cloud:'
    if (la.will_have_clear()):
        wheathr6 = ':sunny:'

    embedColor = random.randint(0, 0xffffff)

    status = weather.get_detailed_status()

    embed = discord.Embed(title="Weather in " + k + " right now:", color=embedColor) #embed title with zip
    embed.add_field(name="Temperature :thermometer:", value=str(weather.get_temperature('celsius')['temp']) + ' C', inline=False) #temperature
    embed.add_field(name="Conditions " + wheathr1 + wheathr2 + wheathr3 + wheathr4 + wheathr5 + wheathr6, value=status, inline=False) #conditions header with emoji conditions
    embed.add_field(name="Wind :wind_blowing_face:", value=str(round(weather.get_wind('miles_hour')['speed'], 1)) + ' mph', inline=False) #wind speed
    embed.add_field(name="Humidity :droplet:", value=str(weather.get_humidity()) + '%', inline=False) #humidity
    embed.add_field(name="Visibility :eye:", value=str(round(weather.get_visibility_distance()/1609.344, 1)) + ' miles', inline=False) #visibility
    embed.set_footer(text='Requested on ' + str(time.ctime())) #prints time

    await ctx.send(embed=embed)

#shows bot info	
@client.command()
async def info(ctx): 

    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="alcebot", description="worst bot lol", color=embedColor)

    # give info about you here
    embed.add_field(name="Author", value="oopsie#1412")
    embed.add_field(name="Users", value=len(ctx.bot.users), inline=False)
    embed.add_field(name="Commands", value=len(ctx.bot.commands), inline=False)
    embed.add_field(name="Processes", value='CPU Usage: ' + str(psutil.cpu_percent()) + "% ", inline=False)
    embed.add_field(name="Purchase Premium", value="[Buy Here](https://buymeacoff.ee/alce)")
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
    embed.add_field(name="a!math <x y z>", value="Gives the operation of **Y** and **Z** using the **X** operation.", inline=False)
    embed.add_field(name="a!greet", value="Gives a nice greet message.", inline=False)
    embed.add_field(name="a!roll", value="Roll a random number from 1 to 6.", inline=False)
    embed.add_field(name="a!translate <x>", value="Translates the phrase into english", inline=False)
    embed.add_field(name="a!weather <zipcode>", value="Gives the latest weather in the area", inline=False)
    embed.add_field(name="a!compliment <x>", value='"Compliments" the tagged user. If nobody is tagged, prints a random compliment', inline=False)
    embed.add_field(name="a!help", value="Gives this message. HEEEEEELP!", inline=False)
    embed.set_footer(text='Requested on ' + str(time.ctime())) #prints time
    
    await ctx.send(embed=embed)

#purge cmd	
@client.command()
async def purge(ctx, number: int):
    """Bulk-deletes messages from the channel."""
    try:
        if ctx.message.author.guild_permissions.administrator:
        
            deleted = await ctx.channel.purge(limit=number+1)
            print('Deleted {} message(s)'.format(len(deleted)))
            logger.info('Deleted {} message(s)'.format(len(deleted)))

        else:
            await ctx.send(config.err_mesg_permission)
    except:
        await ctx.send(config.err_mesg_generic)

#you get a hug, you get a hug, and even you get a hug!	
@client.command()
async def hug(ctx, *, member: discord.Member = None):
    """Hug someone on the server <3"""
    try:
        if member is None:
            await ctx.channel.purge(limit=1)
            await ctx.send(ctx.message.author.mention + " has been hugged!")
            await ctx.send("https://gph.is/g/ajxG084")
        else:
            if member.id == ctx.message.author.id:
                await ctx.channel.purge(limit=1)
                await ctx.send(ctx.message.author.mention + " has hugged themself!")
                await ctx.send("https://gph.is/g/ajxG084")
            else:
                await ctx.channel.purge(limit=1)
                await ctx.send(member.mention + " has been hugged by " + ctx.message.author.mention + "!")
                await ctx.send("https://gph.is/g/ajxG084")

    except:
        await ctx.send(config.err_mesg_generic)

#bot replies
@client.command(aliases=['say'])
async def echo(ctx, *msg):
    """Makes the bot talk."""
    try:
        say = ' '.join(msg)
        await client.delete_message(ctx.message)
        return await ctx.send(say)
    except:
        await ctx.send(config.err_mesg_generic)

#bot replies with tts message
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
            return await ctx.send(":x: ASCII characters only please!")
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

#allows only the owner to change the bots playing status
@client.command(aliases=['game', 'presence'])
async def setgame(ctx, *args):
#Sets the 'Playing' status.
    if(ctx.author.id == 401063536618373121):
        try:
            setgame = ' '.join(args)
            await client.change_presence(status=discord.Status.online, activity=discord.Game(setgame))
            await ctx.send(":ballot_box_with_check: Game name set to: `" + setgame + "`")
            print("Game set to: `" + setgame + "`")
        except:
            await ctx.send(config.err_mesg_generic)
    else:
        await ctx.send(config.err_mesg_permission)

#shows the bot platform
@client.command()
async def botplatform(ctx):
    """Shows what OS the bot is running on."""
    try:
        await ctx.send("The bot is currently running on: ```" + str(platform.platform()) + "```")
    except:
        await ctx.send(config.err_mesg_generic)

#lists all the servers alcebot watches over	
@client.command()
async def serverlist(ctx):
    """List the servers that the bot is active on."""
    x = ', '.join([str(server) for server in client.guilds])
    y = len(client.guilds)
    print("Server list: " + x)
    if y > 40:
        embed = discord.Embed(title="Currently active on " + str(y) + " premium servers:", description=config.err_mesg_generic + "```json\nCan't display more than 40 servers!```", colour=0xFFFFF)
        return await ctx.send(embed=embed)
    elif y < 40:
        embed = discord.Embed(title="Currently active on " + str(y) + " premium servers:", description="```json\n" + x + "```", colour=0xFFFFF)
        return await ctx.send(embed=embed)

#shows banned members on a server
#ban permission required
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
	
#shows info upon a user	
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

#shows websocket latency in milliseconds
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
                logger.info('Failed to load extension {0}\nError: {1}'.format(extension, exc))#

#christmas countdown!
@client.command(aliases=['xmas', 'chrimbo'])
async def christmas(ctx):
    """Christmas countdown!"""
    await ctx.send("**{0}** day(s) left until Christmas day! :christmas_tree:".format(str(diff_cmas.days)))  # Convert the 'diff' integer into a string and say the message

#new year countdown!	
@client.command(aliases=['newyears'])
async def newyear(ctx):
    """new year countdown!"""
    await ctx.send("**{0}** day(s) left until 2020! :confetti_ball:".format(str(diff_ny.days)))  # Convert the 'diff' integer into a string and say the message


@client.command(aliases=['gifmagik'])
async def gmagik(self, ctx, url:str=None, framerate:str=None):
    try:
        url = await self.get_images(ctx, urls=url, gif=True, limit=2)
        if url:
            url = url[0]
        else:
            return
        gif_dir = self.files_path('gif/')
        check = await self.isgif(url)
        if check is False:
            await client.say("Invalid or Non-GIF!")
            ctx.command.reset_cooldown(ctx)
            return
        x = await client.send_message(ctx.message.channel, "ok, processing (this might take a while for big gifs)")
        rand = client.random()
        gifin = gif_dir+'1_{0}.gif'.format(rand)
        gifout = gif_dir+'2_{0}.gif'.format(rand)
        await client.download(url, gifin)
        if os.path.getsize(gifin) > 5000000 and ctx.message.author.id != client.owner.id:
            await client.say(":no_entry: `GIF Too Large (>= 5 mb).`")
            os.remove(gifin)
            return
        try:
            result = await client.loop.run_in_executor(None, self.do_gmagik, ctx, gifin, gif_dir, rand)
        except CancelledError:
            await client.say(':warning: Gmagik failed...')
            return
        if type(result) == str:
            await client.say(result)
            return
        if framerate != None:
            args = ['ffmpeg', '-y', '-nostats', '-loglevel', '0', '-i', gif_dir+'%d_{0}.png'.format(rand), '-r', framerate, gifout]
        else:
            args = ['ffmpeg', '-y', '-nostats', '-loglevel', '0', '-i', gif_dir+'%d_{0}.png'.format(rand), gifout]
        await client.run_process(args)
        await client.upload(gifout, filename='gmagik.gif')
        for image in glob.glob(gif_dir+"*_{0}.png".format(rand)):
            os.remove(image)
        os.remove(gifin)
        os.remove(gifout)
        await client.delete_message(x)
    except Exception as e:
        print(e)

if __name__ == "__main__":  # Load startup extensions, specified in config.py

    if not config.startup_extensions:
        print("No extensions enabled.")
    else:
        print("Loading extensions...")

    #for extension in config.startup_extensions:
     #   try:
      #      client.load_extension(extension)
       #     print("Loaded extension '{0}'".format(extension))
        #    logger.info("Loaded extension '{0}'".format(extension))
         #except Exception as e:
          #   exc = '{}: {}'.format(type(e).__name__, e)
           #  print('Failed to load extension {}\nError: {}'.format(extension, exc))
            # logger.info('Failed to load extension {}\nError: {}'.format(extension, exc))



if __name__ == "__main__":

    # Read client token from "config.py" (which should be in the same directory as this file)
    client.run(config.bbtoken)
    