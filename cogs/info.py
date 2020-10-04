import discord
from discord.ext import commands
import random

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, suggestion, *description):
        ': Suggest a command. Provide the command name and description'
        embedColor = random.randint(0, 0xffffff)
        embed = discord.Embed(title='Command Suggestion', description=f'Suggested by: {ctx.author.mention}\nCommand Name: *{suggestion}*', color=embedColor)
        embed.add_field(name='Description', value=description)
        channel = ctx.guild.get_channel(662755821373095960)
        msg = await channel.send(embed=embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

def setup(bot):
    bot.add_cog(Info(bot))