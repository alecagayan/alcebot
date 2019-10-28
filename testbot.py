import discord
import random
import textblob
import asyncio
import re
import logging
import pyowm

owm = pyowm.OWM('edfb0cd2f5f17a2319a2bdc8b94431cd')

from discord.ext import commands
from textblob import TextBlob

bot = commands.Bot(command_prefix='$')

#array for die images
die_url = ["https://imagen.click/i/3d6d79.png", "https://imagen.click/i/397f38.png", "https://imagen.click/i/4c7a42.png", "https://imagen.click/i/6f4dc6.png", "https://imagen.click/i/a4ca6b.png", "https://imagen.click/i/e617ea.png"]

@bot.event
async def on_ready():

    #sets status    
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with your emotions',))

    #says who its logged in as and gives logs
    logging.basicConfig(level=logging.CRITICAL)
    logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.ERROR)
    print('------')
    logging.basicConfig(level=logging.DEBUG)
    print('------')
    logging.basicConfig(level=logging.INFO)
    print('------')   
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('valid token')
    print('------')

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
async def greet(ctx):
    await ctx.send(":smiley: :wave: Die!")

#prints invite
@bot.command()
async def invite(ctx):
    await ctx.send("https://discordapp.com/oauth2/authorize?client_id=480451439181955093&scope=bot&permissions=8")

#dead body gif
@bot.command()
async def die(ctx):
    await ctx.send("https://media.giphy.com/media/l2YWEbATSPg0YXgGI/giphy.gif")

#roll a die
@bot.command()
async def roll(ctx):
    await ctx.send(die_url[random.randint(1,6)-1])
    
@bot.command()
async def ping(ctx):
    print(bot.latency)
    await ctx.send('Pong! {0}ms'.format(round(bot.latency*1000, 0)))

@bot.command()
async def translate(ctx, a: str, *, b: str):
    opinion = TextBlob(b)
    await ctx.send(opinion.translate(to=a))

@bot.command()
async def sentiment(ctx, *, arg):
    print(arg)
    await ctx.send(arg)
    opinion = TextBlob(arg)
    await ctx.send(opinion.sentiment)

@bot.command()
async def mayb(ctx):
    await ctx.send("hmmm")
    await ctx.send("mayb")
    await ctx.send("what tiem")

@bot.command()
async def belsontrump(ctx):
    await ctx.send("https://imagen.click/i/b8626b.jpg")
    await ctx.send("https://imagen.click/i/846a0e.jpg")

@bot.command()
async def weather(ctx, a):

    wheathr1 = ''
    wheathr2 = ''
    wheathr3 = ''
    wheathr4 = ''
    wheathr5 = ''
    wheathr6 = ''
    wheathrWord = ''

    wethr = owm.weather_at_zip_code(a,'US')
    weather = wethr.get_weather()
    la = owm.three_hours_forecast(a + ', US')
    j = wethr.get_location()
    v = str(weather.get_weather_icon_url())
    k = str(j.get_name())


    if (la.will_have_storm()):
        wheathr1 = ':thunder_cloud_rain:'
    if (la.will_have_snow()):
        wheathr2 = ':snowflake:'
    if (la.will_have_fog()):
        wheathr3 = ':fogblob:'
    if (la.will_have_clear()):
        wheathr6 = ':sunny:'
    elif (la.will_have_rain()):
        wheathr5 = ':cloud_rain:'
    elif (la.will_have_clouds()):
        wheathr4 = ':cloud:'


    embedColor = random.randint(0, 0xffffff)

    status = weather.get_detailed_status()

    embed = discord.Embed(title="Weather in " + k + " right now:", color=embedColor) #embed title with zip
    embed.add_field(name="Temperature :thermometer:", value=str(weather.get_temperature('celsius')['temp']) + ' C', inline=False) #temperature
    embed.add_field(name="Conditions " + wheathr1 + wheathr2 + wheathr3 + wheathr4 + wheathr5 + wheathr6, value=status, inline=False) #conditions header with emoji conditions
    embed.add_field(name="Wind :wind_blowing_face:", value=str(round(weather.get_wind('miles_hour')['speed'], 3)) + ' mph', inline=False) #wind speed
    embed.add_field(name="Humidity :droplet:", value=str(weather.get_humidity()) + '%', inline=False) #humidity
    embed.set_footer(text='alcebot') #prints location

    await ctx.send(embed=embed)
    
@bot.command()
async def info(ctx): 
    embedColor = random.randint(0, 0xffffff)
    embed = discord.Embed(title="alcebot", description="worst bot lol", color=embedColor)

    # give info about you here
    embed.add_field(name="Author", value="oopsie#1412")

    # give users a link to invite bot to their server
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=480451439181955093&scope=bot&permissions=8)")

    await ctx.send(embed=embed)

bot.remove_command('help')

 #adds help command with embed. embed for big brain
@bot.command()
async def help(ctx):
    embedColor = random.randint(0, 0xffffff)

    embed = discord.Embed(title="alcebot", description="horrible bot = horrible commands. List of commands are:", color=embedColor)

    embed.add_field(name="$add X Y", value="Gives the sum of **X** and **Y**.", inline=False)
    embed.add_field(name="$subtract X Y", value="Gives the difference of **X** and **Y**.", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the product of **X** and **Y**.", inline=False)
    embed.add_field(name="$divide X Y", value="Gives the quotient of **X** and **Y**.", inline=False)
    embed.add_field(name="$power X Y", value="Gives **X** to the **Y** power.", inline=False)
    embed.add_field(name="$greet", value="Gives a nice greet message.", inline=False)
    embed.add_field(name="$die", value="Gives a dead body dragging across the floor.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot.", inline=False)
    embed.add_field(name="$roll", value="Roll a random number from 1 to 6.", inline=False)
    embed.add_field(name="$translate X Y", value="Gives translation with **X** as abbreviated language and **Y** as 1 word", inline=False)
    embed.add_field(name="$help", value="Gives this message. HEEEEEELP!", inline=False)

    await ctx.send(embed=embed)


#token
bot.run('token')
