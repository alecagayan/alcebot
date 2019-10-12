import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():

    #sets status    
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('with your emotions',))

    #says who its logged in as
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
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

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Die!")

@bot.command()
async def die(ctx):
    await ctx.send("https://media.giphy.com/media/l2YWEbATSPg0YXgGI/giphy.gif")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="alcebot", description="worst bot lol", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="oopsie#1412")

    # give users a link to invite bot to their server
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=480451439181955093&scope=bot&permissions=8)")

    await ctx.send(embed=embed)

bot.remove_command('help')

 #adds help command with embed. embed for big brain
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="alcebot", description="horrible bot = horrible commands. List of commands are:", color=0xeee657)

    embed.add_field(name="$add X Y", value="Gives the sum of **X** and **Y**.", inline=False)
    embed.add_field(name="$subtract X Y", value="Gives the difference of **X** and **Y**.", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the product of **X** and **Y**.", inline=False)
    embed.add_field(name="$divide X Y", value="Gives the quotient of **X** and **Y**.", inline=False)
    embed.add_field(name="$power X Y", value="Gives **X** to the **Y** power.", inline=False)
    embed.add_field(name="$greet", value="Gives a nice greet message.", inline=False)
    embed.add_field(name="$cat", value="Gives a dead body dragging across the floor.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot.", inline=False)
    embed.add_field(name="$help", value="Gives this message. HEEEEEELP!", inline=False)

    await ctx.send(embed=embed)

#reads message and replies
    async def on_message(self, message):

        if 'cookie' in message.content:
            if not message.author.bot:
                await message.channel.send(':cookie:'.format(message))

        if 'badass santa' in message.content:
            await message.channel.send(':santa: :gun:'.format(message))

        if 'membercount' in message.content:
            await message.channel.send("`{0.name} has this amount of members: {0.member_count}`".format(message))

        if 'poopoo' in message.content:
            await message.channel.send(':poop:'.format(message))

        if 'test12345' in message.content:
            await message.channel.send(':beer:'.format(message))


#token
bot.run('NDgwNDUxNDM5MTgxOTU1MDkz.XaJa5g.X4AksDCN5OuHGdMIyZTfv_WN-JE')
