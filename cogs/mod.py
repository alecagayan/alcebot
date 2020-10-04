import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.ban_members:
            await ctx.guild.ban(member)
            await ctx.send(':white_check_mark: User has been banned from server!') 
        else:
            await ctx.send(":x: **You don't have the permission to use this command.**")

    @commands.command()
    @commands.guild_only()
    async def unban(self, ctx, member: discord.Member):
        if ctx.message.author.guild_permissions.ban_members:
            await ctx.guild.ban(member)
            await ctx.send(':white_check_mark: User has been unbanned from server!') 
        else:
            await ctx.send(":x: **You don't have the permission to use this command.**")

def setup(bot):
    bot.add_cog(Moderation(bot))