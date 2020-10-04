import discord
import textblob
import asyncio
import re
import logger
import logging
import pyowm
import psutil
import time
import json
import io
import platform
import textwrap
import traceback
import copy
import secrets



owm = pyowm.OWM('owm_key')
err_mesg_generic = 'An unknown message has occured! The developer has been notified.'
err_mesg_permission = 'You do not have the proper permissions to complete this action!'
#passcodes definitely should use crypto, and more than just ints
passcode = str(secrets.randbits(256))


if __name__ == "__main__":
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("bot.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

#array for die images
die_url = ["https://imagen.click/i/3d6d79.png", "https://imagen.click/i/397f38.png",
    "https://imagen.click/i/4c7a42.png","https://imagen.click/i/6f4dc6.png",
    "https://imagen.click/i/a4ca6b.png", "https://imagen.click/i/e617ea.png"]

#list for compliments command
compliments = ["your feet are nice", "the dirt under your fingernails is scrumptious",
    "your pupil tastes like a cupcake", "your elbows sound like angels", "your ring finger smells like lilacs",
    "your belly button is as soft as a kitten", "you are not a spoon", "you have teeth",
    "your eyes sparkle more than the sweat in between my toes", "your lips taste like rhinestones",
    "your forehead is a perfect shape, like one of a fluffy dog’s thigh", 
    "the color of your hair makes your kneecap look rather fancy",
    "your trachea is moist and fun", "your kidneys look like all the stars in the sky"]

#list for insults command
insults = ['you smell like rotten granola bars', 'your eyes look like the gum under my shoe',
    'your teeth are as crooked as james charles’ sexuality', 'your armpit hairs look like the prickles on a cactus',
    'i hate the way your style your hair, like a fat sack of eggs', 'your toes smell like butthole',
    'your kneecaps are so weak', 'why does your throat look like that', 'your ears look like shelves',
    "If laughter is the best medicine, your face must be curing the world.", "It's better to let someone think you are an idiot than to open your mouth and prove it.",
    "If I had a face like yours, I'd sue my parents.", "You're so ugly, when your mom dropped you off at school she got a fine for littering.",
    "If I wanted to kill myself I'd climb your ego and jump down to your IQ.", "Brains aren't everything. In your case they're nothing.",
    "Are you always this stupid or is today a special occasion?", "Don't you have a terribly empty feeling - in your skull?",
    "How did you get here? Did someone leave your cage open?", "I'd like to see things from your point of view but I can't seem to get my head that far up my ass.",
    "Have you been shopping lately? They're selling lives, you should go get one.", "The last time I saw something like you, I flushed it.",
    "If ugliness was measured in bricks, you would be the Great Wall of China.", "You want an insult? Look in the mirror!",
    "The story of your life is more insulting than anything I have to say.", "Did a thought cross your mind? It must have been a long and lonely journey...",
    "You'd better hide; the garbage man is coming.", "Roses are red, violets are blue, I have five fingers, the middle one's for you.",
    "I have a text file bigger than your brain in my database. It's 0KB in size.", "You're old enough to remember when emojis were called 'hieroglyphics.'",
    "I don't engage in mental combat with the unarmed.", "Is your ass jealous of the amount of shit that comes out of your mouth?",
    "Your face looks like it caught fire and someone tried to put it out with a fork.","Hey, you have something on your third chin.",
    "I thought a little girl from Kansas dropped a house on you…", "I'm jealous of people that don't know you.", "You bring everyone a lot of joy, when you leave the room.",
    "If you are going to be two faced, at least make one of them pretty.", "If you're going to be a smartarse, first you have to be smart. Otherwise you're just an arse.",
    "Somewhere out there is a tree, tirelessly producing oxygen so you can breathe. I think you owe it an apology.",
    "I don't exactly hate you, but if you were on fire and I had water, I'd drink it.", "If you were on TV, I would change the channel.",
    "You have Diarrhea of the mouth; constipation of the ideas.", "If ugly were a crime, you'd get a life sentence.", "There is no vaccine for stupidity.",
    "Did your parents ever ask you to run away from home?", "Any similarity between you and a human is purely coincidental.", "Keep talking – someday you’ll say something intelligent.",
    "Don’t you love nature, despite what it did to you?", "I'm sure if you studied harder you could get enough qualifications to work as a McDonalds' cleaner.",
    "If I knew you were a cock I would have fed you corn.", "I shouldn't say anything to upset you, I know it's your time of the month.",
    "Has your existence been verified by science yet?", "I don't understand how they could cram so much ugly into one physical form.",
    "You move like a dying yak.", "I'm a pain in your ass because it's the quickest way to your brain"]


@bot.event
async def on_ready():

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('a!'))

    #says who its logged in as and gives logs
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord_alcebot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
  
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('valid token')
    print('passcode: ' + str(passcode))
    print('------')

    
#mass delete messages
@bot.command(aliases=['remove', 'delete'])
async def purge(ctx, number: int):
    if(number <= 10):
            #"""Bulk-deletes messages from the channel."""
            try:
                if ctx.message.author.guild_permissions.administrator:
            
                    deleted = await ctx.channel.purge(limit=number + 1)
                    print('Deleted {} message(s)'.format(len(deleted)))
                    await ctx.send('Deleted ' + number + ' messages')
                    logger.info('Deleted {} message(s)'.format(len(deleted)))
                        
                        
                else:
                    await ctx.send(err_mesg_permission)
            except Exception as e:
                print('alce is a fuckup, here\'s his shitty error:' + e)
                return
    else:
        await ctx.send('Message limit reached! Please pick a number lower than 10')

        
@bot.command()
async def adminpurge(ctx, number: int, code):
    if(code == passcode):
            #"""Bulk-deletes messages from the channel."""
            try:
                if ctx.message.author.guild_permissions.administrator:
            
                    deleted = await ctx.channel.purge(limit=number + 1)
                    print('Deleted {} message(s)'.format(len(deleted)))
                    await ctx.send('Deleted ' + number + ' messages')
                    logger.info('Deleted {} message(s)'.format(len(deleted)))
                        
                else:
                    await ctx.send(err_mesg_permission)
            except Exception as e:
                      print('alce is a fuckup, here\'s his shitty error:' + e)
                      return
    else:
        await ctx.send('Incorrect administrator passcode!')


#lists active servers
@bot.command()
async def serverlist(ctx, a):
    if(passcode == a):
        if ctx.message.author.guild_permissions.administrator:
            #"""List the servers that the bot is active on."""
            embedColor = random.randint(0, 0xffffff)
            await ctx.channel.purge(limit=1)
            x = ', '.join([str(server) for server in bot.guilds])
            y = len(bot.guilds)
            print("Server list: " + x)
            if y > 40:
                embed = discord.Embed(title="Currently active on " + str(y) + " servers:", description=err_mesg_generic + "```json\nCan't display more than 40 servers!```", colour=embedColor)
                return await ctx.send(embed=embed)
            #this is implied you shit
            #elif y < 40:
            embed = discord.Embed(title="Currently active on " + str(y) + " servers:", description="```json\n" + x + "```", colour=embedColor)
            return await ctx.send(embed=embed)
    else:
        await ctx.send('Incorrect administrator passcode!')

        
#hugs intended person
@bot.command()
async def hug(ctx, *, member: discord.Member = None):
    """Hug someone on the server <3"""
    try:
        if member is None:
            await ctx.send(ctx.message.author.mention + " has been hugged!")
            await ctx.send("https://gph.is/g/ajxG084")
        else:
            if member.id == ctx.message.author.id:
                await ctx.send(ctx.message.author.mention + " has hugged themself!")
                await ctx.send("https://gph.is/g/ajxG084")
            else:
                await ctx.send(member.mention + " has been hugged by " + ctx.message.author.mention + "!")
                await ctx.send("https://gph.is/g/ajxG084")

    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e)
        await ctx.send(err_mesg_generic)

        
#add
@bot.command()
async def add(ctx, a: float, b: float):
    await ctx.send(a+b)

    
#subtract
@bot.command()
async def subtract(ctx, a: float, b: float):
    await ctx.send(a-b)

    
#multiply
@bot.command()
async def multiply(ctx, a: float, b: float):
    await ctx.send(a*b)

    
#divide
@bot.command()
async def divide(ctx, a: float, b: float):
    await ctx.send(a/b)

    
#exponent
@bot.command()
async def power(ctx, a: float, b: float):
    await ctx.send(a**b)

    
#tells you to die
@bot.command()
async def cleck(ctx):
    await ctx.send("https://imagen.click/i/7cd655.png")

    
@bot.command()
async def github(ctx):
    await ctx.send("https://github.com/oopsie1412/alcebot")

    
#prints invite
@bot.command()
async def invite(ctx):
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=480451439181955093&scope=bot&permissions=8")

    
#roll a die
@bot.command()
async def roll(ctx):
    await ctx.send(die_url[secrets.randbelow(len(die_url)-1)])

    
@bot.command()
async def compliment(ctx, *, member: discord.Member = None):
    
    compliment
    try:
        if member is None:
            await ctx.send(ctx.message.author.mention + " " + str(compliments[secrets.randbelow(len(compiments)-1)]))
        else:
            await ctx.send(member.mention + " " + str(compliments[secrets.randbelow(len(compiments)-1)]))
    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e
        await ctx.send(err_mesg_generic)

              
@bot.command()
async def insult(ctx, *, member: discord.Member = None):
    """insults"""
    try:
        if member is None:
            await ctx.send(ctx.message.author.mention + " " + str(insults[secrets.randbelow(len(insults)-1]))
        else:
            await ctx.send(member.mention + " " + str(insults[secrets.randbelow(len(insults)-1]))
    except Exception as e:
        print('alce is a fuckup, here\'s his shitty error:' + e)
        await ctx.send(err_mesg_generic)

                                                              
@bot.command()
async def pasta(ctx):
    await ctx.send('cut em thiccque daddy')

                                                              
@bot.command()
async def botplatform(ctx, a):
    if(passcode == a):
        ##"""Shows what OS the bot is running on."""
        try:
            await ctx.send("The bot is currently running on: ```" + str(platform.platform()) + "```")
        except:
            await ctx.send(err_mesg_generic)
    else:
        await ctx.send('Incorrect administrator passcode!')

                                                              
#ping
@bot.command()
async def ping(ctx):
    print(bot.latency)
    await ctx.send('Pong! {0}ms websocket latency'.format(round(bot.latency*1000, 3)))

                                                              
#translate
@bot.command()
async def credit(ctx):
    embedColor = secrets.randbelow(0xFFFFFF)
    embed = discord.Embed(title="Thanks to these people:", color=embedColor)

    embed.add_field(name="Author", value='oopsie#1412')
    embed.add_field(name="GitHub Contributors", value='lincoln-bridge, gidoBOSSftw5731')
    embed.add_field(name="Discord Contributors", value='Motions#5324, GidoBOSSftw5731#6422, chickenramen#7173')
    embed.add_field(name="Beta Testers", value='oopsie#1412')


    await ctx.send(embed=embed)

                                                              
#sentiment
@bot.command()
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
@bot.command()
async def hugeveryone(ctx):
    await ctx.send("@here has been hugged by " + ctx.message.author.mention + "!")

                                                              
@bot.command()
async def suggest(ctx, *, a):
    await ctx.send("Thank you for the suggestion! I will get back to you soon!")
    print ("suggestion: " + a)

                                                              
@bot.command()
async def belsontrump(ctx):
    await ctx.send("https://imagen.click/i/b8626b.jpg")
    await ctx.send("https://imagen.click/i/846a0e.jpg")

                                                              
@bot.command()
async def weather(ctx, a):

    print('{0}ms'.format(round(bot.latency*1000, 3)))

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

                                                              
@bot.command()
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

                                                             
bot.remove_command('help')

                                                              
 #adds help command with embed. embed for big brain
@bot.command()
# can this be renamed? I dont like python enough to know
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


#token
bot.run('token')

