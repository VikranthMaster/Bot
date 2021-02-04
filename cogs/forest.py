import discord
from discord.ext import commands
import json
from discord import DMChannel

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

class Forest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Forest cog loaded")
    

    @commands.command()
    async def create(self,ctx, code, stime, duration):
        embed = discord.Embed(
            title="Forest",
            color = discord.Color.blue()
            )   
        try:
            if len(code) == 7 and len(stime) < 6 and len(duration) < 4:
            # await ctx.send(discord.utils.get(ctx.guild.roles, name="Forest").mention)
                embed.add_field(name = "Hosted by: ", value = ctx.message.author.mention, inline = False)
                embed.add_field(name = "Code: ", value = code, inline = False)
                embed.add_field(name = "Starting Time: ", value = stime, inline = False)
                embed.add_field(name = "Duration: ", value = duration, inline = False)
                embed.add_field(name = "Link:", value = f"https://forestapp.cc/join-room?token={code}", inline = False)
                msg = await ctx.channel.send(embed=embed)
                reaction = await msg.add_reaction("🌲")
                

                user = await client.fetch_user(ctx.message.author.id)
                await DMChannel.send(user, f"Hello there, You have hosted a forest session at **{stime}** and code is **{code}** of **{duration}**mins")
            
            else:
                await ctx.send("The parameters which u have sent is not appropriate. Pls check it again")
        except:
            await ctx.send("Sorry, but give the full parameters required or type >help for the more commands")

def setup(client):
  client.add_cog(Forest(client))
  print("Forest cog is loaded")