import discord
from discord.ext import commands
import json

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

class changePrefix(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("changePrefix cog loaded successfully")

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        with open('prefixes.json','r') as f:
            prefixes = json.load(f)
        
        prefixes[str(guild.id)] = ">"

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        with open('prefixes.json','r') as f:
            prefixes = json.load(f)
        
        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def changeprefix(self,ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        
        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Prefix is changed to ``{prefix}``")
    
def setup(client):
    client.add_cog(changePrefix(client))