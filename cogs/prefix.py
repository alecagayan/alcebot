import discord
from discord.ext import commands
import json

async def is_guild_owner(ctx):
    return ctx.message.author.guild_permissions.administrator

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, *, pre):
        with open(r"/opt/alcebot/alcebot/prefixes.json", 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = pre
        await ctx.send("Prefix set to `" + pre + "`")

        with open(r"/opt/alcebot/alcebot/prefixes.json", 'w') as f:
            json.dump(prefixes, f, indent=4)

def setup(bot):
    bot.add_cog(Prefix(bot))
