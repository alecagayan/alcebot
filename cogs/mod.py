import discord

from io import BytesIO

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberID):
        if ctx.message.author.guild_permissions.ban_members:
            await ctx.guild.ban(discord.Object(id=member))
            await ctx.send(':white_check_mark: User has been banned from server!') 
        else:
            await ctx.send(":x: **You don't have the permission to use this command.**")

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def unban(self, ctx, member: MemberID):
        if ctx.message.author.guild_permissions.ban_members:
            await ctx.guild.unban(discord.Object(id=member))
            await ctx.send(':white_check_mark: User has been unbanned from server!') 
        else:
            await ctx.send(":x: **You don't have the permission to use this command.**")

def setup(bot):
    bot.add_cog(Moderation(bot))