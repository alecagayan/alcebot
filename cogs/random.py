import discord
import aiohttp
import sr_api
import random

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
    async def base64(self, ctx, function, *, text):
        srapi = sr_api.Client()
        if(function == 'encode'):
            result = await srapi.encode_base64(text)
            await ctx.send(result)
        else:
            result = await srapi.decode_base64(text)
            await ctx.send(result)

    @commands.command()
    @commands.guild_only()
    async def lyrics(self, ctx, *, title):
        srapi = sr_api.Client()
        response = await srapi.get_lyrics(title)
        lyric = response.lyrics
        finallyric = (lyric[:1020] + '...') if len(lyric) > 1020 else lyric

        embedColor = random.randint(0, 0xffffff)
        embed = discord.Embed(title="Lyrics of " + response.title + " by " + response.author + ":", color=embedColor)
        embed.set_thumbnail(url=response.thumbnail)
        embed.add_field(name = response.title, value=finallyric, inline=True)
        embed.add_field(name = 'Full lyrics: ', value=response.link, inline=False)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Random(bot))