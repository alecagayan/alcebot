import pyowm
from pyowm.utils import timestamps
from pyowm.owm import OWM
import config
import random
import discord
from discord.ext import commands
import datetime

owm = pyowm.OWM('edfb0cd2f5f17a2319a2bdc8b94431cd')

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def weather(self, ctx, a, t = None):
        comma = ','
        mgr = owm.weather_manager()

        if comma in a:
            observation = mgr.weather_at_place(a)
        else:
            observation = mgr.weather_at_zip_code(a, 'US')

        weather = observation.weather
        embedColor = random.randint(0, 0xffffff)

        if(t == 'f'):
            cf = 'fahrenheit'
            label = ' F'
        elif(t == 'fahrenheit'):
            cf = 'fahrenheit'
            label = ' F'
        elif(t == 'celsius'):
            cf = 'celsius'
            label = ' C'
        else:
            cf = 'celsius'
            label = ' C'

        embed = discord.Embed(title="Weather in " + a + " right now:", color=embedColor) #embed title with zip
        embed.add_field(name="Temperature :thermometer:", value=str(weather.temperature(cf)['temp']) + label, inline=True) #temperature
        embed.add_field(name="Feels like :snowflake:", value=str(weather.temperature(cf)['feels_like']) + label, inline=True) #temperature
        embed.add_field(name="Conditions :white_sun_rain_cloud:", value=weather.detailed_status, inline=True) #conditions header with emoji conditions
        embed.add_field(name="Wind Speed :wind_blowing_face:", value=str(round(weather.wind('miles_hour')['speed'], 1)) + ' mph', inline=True) #wind speed
        embed.add_field(name="Wind Direction :dash:", value=str(round(weather.wind('miles_hour')['deg'], 1)) + '°', inline=True) #wind speed
        embed.add_field(name="Humidity :droplet:", value=str(weather.humidity) + '%', inline=True) #humidity
        embed.add_field(name="Visibility :eye:", value=str(round(weather.visibility_distance/1609.344, 1)) + ' miles', inline=True) #visibility
        embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def forecast(self, ctx, a, t = None):
        comma = ','
        mgr = owm.weather_manager()

        if comma in a:
            observation = mgr.forecast_at_place(a, '3h').forecast
        else:
            observation = mgr.forecast_at_place(a + ',US', '3h').forecast

        weather = observation.weather
        embedColor = random.randint(0, 0xffffff)

        if(t == 'f'):
            cf = 'fahrenheit'
            label = ' F'
        elif(t == 'fahrenheit'):
            cf = 'fahrenheit'
            label = ' F'
        elif(t == 'celsius'):
            cf = 'celsius'
            label = ' C'
        else:
            cf = 'celsius'
            label = ' C'

        tomorrow = timestamps.tomorrow()                                   # datetime object for tomorrow
        weather = observation.get_weather_at(tomorrow)
        await ctx.send(weather)

#        embed = discord.Embed(title="Daily forecast for  " + a + ": ", color=embedColor) #embed title with zip
#        embed.add_field(name="Temperature :thermometer:", value=str(weather.temperature(cf)['temp']) + label, inline=True) #temperature
#        embed.add_field(name="Feels like :snowflake:", value=str(weather.temperature(cf)['feels_like']) + label, inline=True) #temperature
#        embed.add_field(name="Conditions :white_sun_rain_cloud:", value=weather.detailed_status, inline=True) #conditions header with emoji conditions
#        embed.add_field(name="Wind Speed :wind_blowing_face:", value=str(round(weather.wind('miles_hour')['speed'], 1)) + ' mph', inline=True) #wind speed
#        embed.add_field(name="Wind Direction :dash:", value=str(round(weather.wind('miles_hour')['deg'], 1)) + '°', inline=True) #wind speed
#        embed.add_field(name="Humidity :droplet:", value=str(weather.humidity) + '%', inline=True) #humidity
#        embed.add_field(name="Visibility :eye:", value=str(round(weather.visibility_distance/1609.344, 1)) + ' miles', inline=True) #visibility
#        embed.set_footer(text='Requested on ' + str(datetime.datetime.now())) #prints time
#        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Weather(bot))