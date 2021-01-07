import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import platform
import sys
import os
import random
import requests
import json
import time
import pyowm
import datetime
from time import ctime
import config
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import urllib
import urllib.request
import logging
import psutil
import aiohttp

now = datetime.datetime.now()
start_time = time.time()
datetime.datetime.today()  # Days until Christmas
passcode = str(random.randint(10000000000000000000,99999999999999999999))
devID = 401063536618373121
owm = pyowm.OWM(config.owm_key)
filename_state = "/opt/alcebot/alcebot/us-states.csv"
filename_county = "/opt/alcebot/alcebot/us-counties.csv"
county_graph = '/opt/alcebot/alcebot/plot-county.png'
state_graph = '/opt/alcebot/alcebot/plot-state.png'

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

@client.command()
async def time(ctx):
    await ctx.send(datetime.datetime.now())

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
async def compliment(ctx, member: discord.Member = None):
    await ctx.send(member.mention + " " + random.choice(config.compliments))

#sends a compliment from compliment list in config.py
@client.command()
async def insult(ctx, member: discord.Member = None):
    await ctx.send(member.mention + " " + random.choice(config.insults))  # Mention the user and say the insult

@client.command()
async def die(ctx):
    if(ctx.author.id == 401063536618373121):
        await ctx.send("Drinking bleach.....")
        await client.close()
    else:
        await ctx.send(config.err_mesg_permission)

@client.command()
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    embed = discord.Embed(colour=ctx.message.author.top_role.colour)
    embed.add_field(name="Uptime", value=text)
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))

    await ctx.send(embed=embed)

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
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))
    embed.add_field(name='Name', value=ctx.guild.name, inline=True)
    embed.add_field(name='ID', value=ctx.guild.id, inline=True)
    embed.add_field(name='Owner', value=ctx.guild.owner, inline=True)
    embed.add_field(name='Region', value=ctx.guild.region, inline=True)
    embed.add_field(name='Member Count', value=ctx.guild.member_count, inline=True)
    embed.add_field(name='Creation', value=ctx.guild.created_at.strftime('%d.%m.%Y'), inline=True)
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))
    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    """
    Pings the bot.
    """
    joke = random.choice(["not actually pinging server...", "hey bb", "what am I doing with my life",
                            "JAMB is a dank music bot tbh", "I'd like to thank the academy for this award",
                            "The NSA is watching 👀", "`<Insert clever joke here>`", "¯\_(ツ)_/¯", "(づ｡◕‿‿◕｡)づ",
                            "I want to believe...", "Hypesquad is a joke", "Robino pls",
                            "Seth got arrested again...", "aaaaaaaaaaaAAAAAAAAAA", "owo",
                            "uwu", "meme team best team", "made with dicksword dot pee why", "I'm running out of "
                                                                                            "ideas here",
                            "am I *dank* enough for u?", "this is why we can't have nice things. come on",
                            "You'll understand when you're older...", "\"why\", you might ask? I do not know...",
                            "I'm a little tea pot, short and stout", "I'm not crying, my eyeballs "
                                                                    "are sweating!",
                            "When will the pain end?"])
    ping_msg = await ctx.send("Pinging Server...")
    await ping_msg.edit(content=joke + f" // ***{client.latency*1000:.0f}ms***")


#credits contributors
@client.command()
async def credit(ctx):
    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="Thanks to these people:", color=embedColor)

    embed.add_field(name="Author", value='oopsie#1412')
    embed.add_field(name="GitHub Contributors", value='lincoln-bridge, gidoBOSSftw5731, iCrazyBlaze, rgb4')
    embed.add_field(name="Discord Contributors", value='always#5324, GidoBOSSftw5731#6422, chickenramen#7173')
    embed.add_field(name="Beta Testers", value='oopsie#1412')
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))

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
        embed.set_footer(text='Requested on ' + str(datetime.datetime.now()))

        await ctx.send(embed=embed)
    else:
        await ctx.send(config.err_mesg_permission)

#marks a suggestion in log
@client.command()
async def suggestion(ctx, *, a):
    await ctx.send("Thank you for the suggestion! I will get back to you soon!")
    print ("suggestion: " + a)

#Shows the current weather at zip code	
@client.command()
async def weather(ctx, a, t = None):
    comma = ','
    mgr = owm.weather_manager()

    if comma in a:
        observation = mgr.weather_at_place(a)
    else:
        observation = mgr.weather_at_zip_code(a, 'US')

    weather = observation.weather
    embedColor = random.randint(0, 0xffffff)

    if(t == 'f'):
        cf = 'fahrenheit'
        label = ' F'
    elif(t == 'fahrenheit'):
        cf = 'fahrenheit'
        label = ' F'
    elif(t == 'celsius'):
        cf = 'celsius'
        label = ' C'
    else:
        cf = 'celsius'
        label = ' C'

    embed = discord.Embed(title="Weather in " + a + " right now:", color=embedColor) #embed title with zip
    embed.add_field(name="Temperature :thermometer:", value=str(weather.temperature(cf)['temp']) + label, inline=True) #temperature
    embed.add_field(name="Feels like :snowflake:", value=str(weather.temperature(cf)['feels_like']) + label, inline=True) #temperature
    embed.add_field(name="Conditions :white_sun_rain_cloud:", value=weather.detailed_status, inline=True) #conditions header with emoji conditions
    embed.add_field(name="Wind Speed :wind_blowing_face:", value=str(round(weather.wind('miles_hour')['speed'], 1)) + ' mph', inline=True) #wind speed
    embed.add_field(name="Wind Direction :dash:", value=str(round(weather.wind('miles_hour')['deg'], 1)) + '°', inline=True) #wind speed
    embed.add_field(name="Humidity :droplet:", value=str(weather.humidity) + '%', inline=True) #humidity
    embed.add_field(name="Visibility :eye:", value=str(round(weather.visibility_distance/1609.344, 1)) + ' miles', inline=True) #visibility
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
    await ctx.send(embed=embed)
    #await ctx.send('foobar')

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
    embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    await ctx.send(embed=embed)

client.remove_command('help')

@client.command()
async def help(ctx):

    embedColor = random.randint(0, 0xffffff)

    message = await ctx.send("Select a page by reacting below!")
    # getting the message object for editing and reacting

    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")

    with open('prefixes.json', 'r') as f:
        prefixes=json.load(f)
        prefix = prefixes[str(ctx.guild.id)]

    embed1 = discord.Embed(title="Help Page 1/5", description="Need help? Look below", color=embedColor)
    embed1.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed1.add_field(name=prefix + "time", value="Reads the time in EST", inline=False)
    embed1.add_field(name=prefix + "math <x y z>", value="Gives the operation of **Y** and **Z** using the **X** operation.", inline=False)
    embed1.add_field(name=prefix + "covid <state/county> <name>", value="Gives coronavirus statistics", inline=False)
    embed1.add_field(name=prefix + "github", value="Gives the link to bot code", inline=False)
    embed1.add_field(name=prefix + "invite", value="Sends the bot invite", inline=False)
    embed1.add_field(name=prefix + "roll", value='Rolls a die', inline=False)
    embed1.add_field(name=prefix + "compliment", value="Compliments a user you tag. If nobody is tagged, a compliment will be printed", inline=False)
    embed1.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed2 = discord.Embed(title="Help Page 2/5", description="Need help? Look below!", color=embedColor)
    embed2.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed2.add_field(name=prefix + "insult", value="Insults a user you tag. If nobody is tagged, an insult will be printed", inline=False)
    embed2.add_field(name=prefix + "uptime", value="Shows the uptime of the bot", inline=False)
    embed2.add_field(name=prefix + "xkcd", value="Random XKCD comic", inline=False)
    embed2.add_field(name=prefix + "server", value="Gives server info", inline=False)
    embed2.add_field(name=prefix + "ping", value="Pings the bot", inline=False)
    embed2.add_field(name=prefix + "credit", value='Who made alcebot? Time to find out!', inline=False)
    embed2.add_field(name=prefix + "hug", value="Hug anyone in the server!", inline=False)
    embed2.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed3 = discord.Embed(title="Help Page 3/5", description="Need help? Look below", color=embedColor)
    embed3.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed3.add_field(name=prefix + "premium", value="You already have premium!", inline=False)
    embed3.add_field(name=prefix + "suggestion <suggestion>", value="Suggest a new feature or bug fix", inline=False)
    embed3.add_field(name=prefix + "weather <zip code> <c or f>", value="Get the weather at your location", inline=False)
    embed3.add_field(name=prefix + "info", value="Gives basic bot info", inline=False)
    embed3.add_field(name=prefix + "purge <num of msgs>", value="Purge a certain number of messages", inline=False)
    embed3.add_field(name=prefix + "netdiskcpu", value='Get info about the bot computer (owner only)', inline=False)
    embed3.add_field(name=prefix + "fancify <text>", value="Makes text 𝓕𝓐𝓝𝓒𝓨", inline=False)
    embed3.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed4 = discord.Embed(title="Help Page 4/5", description="Need help? Look below", color=embedColor)
    embed4.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed4.add_field(name=prefix + "botplatform", value="Gives a little info about the platform the bot runs on", inline=False)
    embed4.add_field(name=prefix + "getbans", value="Shows a list of banned users", inline=False)
    embed4.add_field(name=prefix + "userinfo", value="Gives info on a user", inline=False)
    embed4.add_field(name=prefix + "christmas", value="Christmas countdown!", inline=False)
    embed4.add_field(name=prefix + "newyear", value="New Year countdown!", inline=False)
    embed4.add_field(name=prefix + "ban", value='Bans the tagged user', inline=False)
    embed4.add_field(name=prefix + "unban", value="Unbans the tagged user", inline=False)
    embed4.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    embed5 = discord.Embed(title="Help Page 5/5", description="Need help? Look below", color=embedColor)
    embed5.add_field(name="Support server", value="[Invite link](https://discord.gg/MJejP9q)")
    embed5.add_field(name=prefix + "prefix <prefix>", value="Changes the bot prefix", inline=False)
    embed5.add_field(name=prefix + "enlarge <user>", value="Enlarge a user's profile photo", inline=False)
    embed5.add_field(name=prefix + "servericon", value="Shows the server's icon", inline=False)
    embed5.add_field(name=prefix + "mods", value="**In Beta**. Shows the moderators that are online", inline=False)
    embed5.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "1️⃣":
                await message.edit(embed=embed1)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "2️⃣":
                await message.edit(embed=embed2)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "3️⃣":
                await message.edit(embed=embed3)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "4️⃣":
                await message.edit(embed=embed4)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "5️⃣":
                await message.edit(embed=embed5)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds

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
    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e)
    return


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

    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e)
    return

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

    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e)
    return


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
        except Exception as e:
            print('alce is a fuckup, here\'s his shitty error:' + e)
        return
    else:
        await ctx.send(config.err_mesg_permission)


#shows the bot platform
@client.command()
async def botplatform(ctx):
    """Shows what OS the bot is running on."""
    try:
        await ctx.send("The bot is currently running on: ```" + str(platform.platform()) + "```")
    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e)
    return


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
    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e)
    return


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
    diff_cmas = datetime.datetime(now.year, 12, 25) - \
    """Christmas countdown!"""
    await ctx.send("**{0}** day(s) left until Christmas day! :christmas_tree:".format(str(diff_cmas.days)))  # Convert the 'diff' integer into a string and say the message


#new year countdown!	
@client.command(aliases=['newyears'])
async def newyear(ctx):
    diff_ny = datetime.datetime(now.year + 1, 1, 1) - \
    """new year countdown!"""
    await ctx.send("**{0}** day(s) left until 2020! :confetti_ball:".format(str(diff_ny.days)))  # Convert the 'diff' integer into a string and say the message

if __name__ == "__main__":

    # Read client token from "config.py" (which should be in the same directory as this file)
    client.run(config.bbtoken)
    
