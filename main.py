import discord
import random
import textblob
import asyncio
import re
import logging

from discord.ext import commands
from textblob import TextBlob



bot = commands.Bot(command_prefix='$')

#array for die images
die_url = ["https://imagen.click/i/3d6d79.png", "https://imagen.click/i/397f38.png", "https://imagen.click/i/4c7a42.png", "https://imagen.click/i/6f4dc6.png", "https://imagen.click/i/a4ca6b.png", "https://imagen.click/i/e617ea.png"]

@bot.event
async def on_ready():

    #sets status    
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with your emotions',))

    #says who its logged in as

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
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

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
async def info(ctx): 
    embed = discord.Embed(title="alcebot", description="worst bot lol", color=0x7289da)

    # give info about you here
    embed.add_field(name="Author", value="oopsie#1412")

    # give users a link to invite bot to their server
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=480451439181955093&scope=bot&permissions=8)")

    await ctx.send(embed=embed)

bot.remove_command('help')

 #adds help command with embed. embed for big brain
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="alcebot", description="horrible bot = horrible commands. List of commands are:", color=0x7289da)

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
bot.run('NDgwNDUxNDM5MTgxOTU1MDkz.XaJ7ZA.T2z7Hxen-SBclxCYBx5FDcHmyco')
