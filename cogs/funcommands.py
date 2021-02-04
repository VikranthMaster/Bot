import discord
from discord.ext import commands
import json
import random
import aiohttp
import giphy_client
from giphy_client.rest import ApiException
import requests

cmds = ["Duh, Stop talking to me and get back to work.","Who the hell summoned me?! I am sleeping !!","Bruh, what do you want ?!","Hey sorry i was so mean !", "Heya whats up ?", "Hey handsome !", "Yo! Dude sup"]

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun cog loaded")
    
    @commands.command()
    async def clear(self,ctx, amount=5):
      await ctx.channel.purge(limit=amount)


    @commands.command()
    async def poll(self,ctx, *, message):
        emb = discord.Embed(title=" POLL", description=f"{message}")
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.command()
    async def meme(self,ctx):
        embed = discord.Embed(color=discord.Color.blue())

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 30)]['data']['url'])
                await ctx.send(embed=embed)
    
    @commands.command()
    async def gif(self,ctx,*,q="Smile"):
      api_key = "35lYrouR4b4FQWO4Z5IOo0gaRQN4YCOs"
      api_instance = giphy_client.DefaultApi()

      try:
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating="g")
        lst = list(api_response.data)
        giff = random.choice(lst)
      
      except ApiException as e:
        print("Exception when calling Api")
      
      embed = discord.Embed(title=q)
      embed.set_image(url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")

      await ctx.channel.send(embed=embed)

      @commands.command()
      async def ping(self,ctx):
        embed = discord.Embed(
            color= discord.Color.blue()
        )
        embed.add_field(name = "Ping", value= "Pong! {0}".format(round(client.latency, 1)), inline = False)

        await ctx.send(embed=embed)

      @commands.Cog.listener()
      async def on_message(self, message):
        if message.content.find("Time to put down your phone and get back to work! Enter my room code") != -1:
          await message.channel.send(f"Awww...please use me..pls {message.author.mention}")
        if client.user.mentioned_in(message):
          await message.channel.send(random.choice(cmds))
      
      @commands.command(alias=['user','info'])
      async def whois(ctx, member : discord.Member):
          embed = discord.Embed(title=member.name, description=member.mention, color=discord.Color.blue())
          embed.add_field(name="ID", value=member.id, inline=True)
          await ctx.send(embed=embed)

      @commands.command()
      async def users(ctx):
          embed = discord.Embed(color=discord.Color.blue(), title=f"{ctx.guild.name}")
          embed.add_field(name="Total memebers in this server are ",value=f"{ctx.guild.member_count}")
          await ctx.send(embed=embed)

      @commands.command()
      async def kick(ctx, member : discord.Member, *, reason = None):
          await member.kick(reason=reason)

      @commands.command()
      async def dm(ctx, member:discord.Member):
        await ctx.send("what do you want to say")
        def check(msg):
          return msg.author.id == ctx.message.author.id

        message = await client.wait_for('message',check=check)
        await ctx.send(f'sent message to {member.mention}')

        await member.send(f'{ctx.author.mention} Has a message for you:\n {message.content}')


      @commands.command()
      async def quote(ctx):
        results = requests.get("https://type.fit/api/quotes/").json()
        num = random.randint(1,1500)
        content = results[num]["text"]
        embed = discord.Embed(color= discord.Color.blue())
        embed.add_field(name="Quote:", value=f"*{content}*")

        await ctx.send(embed=embed)
      
    #   @commands.command(aliases=["fact"])
    #   async def animal_fact(self,ctx,animal:str):
    #     if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
		# 	    fact_url = f"https://some-random-api.ml/facts/{animal}"
		# 	    image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

		# 	  async with request("GET", image_url, headers={}) as response:
		# 	  	if response.status == 200:
		# 			  data = await response.json()
		# 			  image_link = data["link"]

		# 		  else:
		# 			  image_link = None

		# 	  async with request("GET", fact_url, headers={}) as response:
		# 		  if response.status == 200:
		# 			  data = await response.json()

		# 			  embed = Embed(title=f"{animal.title()} fact",
		# 						  description=data["fact"],
		# 						  colour=ctx.author.colour)
		# 			  if image_link is not None:
		# 				  embed.set_image(url=image_link)
		# 			  await ctx.send(embed=embed)

		# 		else:
		# 			await ctx.send(f"API returned a {response.status} status.")

		# else:
		# 	await ctx.send("No facts are available for that animal.")

def setup(client):
  client.add_cog(Fun(client))
  print("Fun cog is loaded")

  