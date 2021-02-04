import discord
from discord.ext import commands
import json
import requests

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

api_key = "5e74111393bae2a5c24675da1604b841"

key_features = {
    'temp' : "Temperature",
    'feels_like' : "Feels Like",
    'temp_min' : 'Minimum Temperature',
    'temp_max' : 'Maximum Temperature',
    'humidity' : 'Humidity',
    'pressure' : 'Pressure' 
}

def parse_data(data):
    data = data['main']
    return data

def weather_message(data, location):
    location = location.title()
    message = discord.Embed(title=f"{location} Weather", description=f"We have weather data for {location}", color = discord.Color.blue())
    for key in data:
        message.add_field(name=key_features[key], value=str(data[key]), inline=False)
    return message

def error_message(location):
    location = location.title()
    return discord.Embed(title="Error", description=f"There is no location like that or there was a error receving the data for {location}", color = discord.Color.blue())

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather Cog is loaded")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author != client.user and message.content.startswith("w."):
            location = message.content.replace("w.", "").lower()
            if len(location) >= 1:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
            try:
                data = json.loads(requests.get(url).content)
                data = parse_data(data)
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))


def setup(client):
  client.add_cog(Weather(client))
  print("Weather cog is loaded")
