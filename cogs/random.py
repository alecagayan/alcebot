import discord
import aiohttp
import sr_api

from io import BytesIO
from discord.ext import commands


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.guild_only()
    async def enlarge(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        user = user or ctx.author
        await ctx.send(user.avatar_url_as(size=1024))

    @commands.command(aliases=["servericon"])
    async def server_avatar(self, ctx):
        """ Get the current server icon """
        if not ctx.guild.icon:
            return await ctx.send("This server does not have a avatar...")
        await ctx.send(ctx.guild.icon_url_as(size=1024))

    @commands.command()
    @commands.guild_only()
    async def mods(self, ctx):
        """ Check which mods are online on current guild """
        message = ""
        online, idle, dnd, offline = [], [], [], []

        for user in ctx.guild.members:
            if ctx.channel.permissions_for(user).kick_members or \
               ctx.channel.permissions_for(user).ban_members:
                if not user.bot and user.status is discord.Status.online:
                    online.append(f"**{user}**")
                if not user.bot and user.status is discord.Status.idle:
                    idle.append(f"**{user}**")
                if not user.bot and user.status is discord.Status.dnd:
                    dnd.append(f"**{user}**")
                if not user.bot and user.status is discord.Status.offline:
                    offline.append(f"**{user}**")

        if online:
            message += f"🟢 {', '.join(online)}\n"
        if idle:
            message += f"🟡 {', '.join(idle)}\n"
        if dnd:
            message += f"🔴 {', '.join(dnd)}\n"
        if offline:
            message += f"⚫ {', '.join(offline)}\n"

        await ctx.send(f"Mods in **{ctx.guild.name}**\n{message}")

    @commands.command()
    @commands.guild_only()
    async def base64(self, ctx, function, *, text):
        srapi = sr_api.Client()

        if(function == 'encode'):
            result = await srapi.encode_base64(text)
            await ctx.send(result)
        else:
            result = await srapi.decode_base64(text)
            await ctx.send(result)

def setup(bot):
    bot.add_cog(Random(bot))