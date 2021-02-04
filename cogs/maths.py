import discord
from discord.ext import commands
import json

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

def add(x,y):
  result = int(x) + int(y)
  return result

def subtract(x,y):
  result = int(x) - int(y)
  return result

def multiply(x,y):
  result = int(x) * int(y)
  return result

def divide(x,y):
  result = int(x) / int(y)
  return result

class Maths(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Math cog loaded successfully")
    
    @commands.command()
    async def add(self,ctx,num1,num2):
      # add = add(num1,num2)
      await ctx.send(f"Your sum is ``{add(num1,num2)}``")
    
    @commands.command(aliases=["sub"])
    async def subtract(self,ctx,num1,num2):
      # sub = subtract(num1,num2)
      await ctx.send(f"Your Difference is ``{subtract(num1,num2)}``")
    
    @commands.command(aliases=["multi"])
    async def multiply(self,ctx,num1,num2):
      # mult = multiply(num1,num2)
      await ctx.send(f"Your product is ``{multiply(num1,num2)}``")

    @commands.command(aliases=["div"])
    async def divide(self,ctx,num1,num2):
      # div = divide(num1,num2)
      await ctx.send(f"Your quotient is ``{divide(num1,num2)}``") 
        
def setup(client):
    client.add_cog(Maths(client))
    print("Maths cog is loaded")
