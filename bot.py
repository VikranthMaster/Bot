import discord
from discord.ext import commands
from discord import DMChannel
import os
import json
import asyncio
import sqlite3
import math 
import random


client = commands.Bot(command_prefix = ">")

cmds = ["Duh, Stop talking to me and get back to work.","Who the hell summoned me?! I am sleeping !!","Bruh, what do you want ?!","Hey sorry i was so mean !", "Heya whats up ?", "Hey handsome !", "Yo! Dude sup"]

client.remove_command("help")

@client.event
async def on_ready():
  db = sqlite3.connect('main.sqlite')
  cursor = db.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
    guild_id TEXT,
    msg TEXT, 
    channel_id TEXT
    )
  ''')

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS levels(
      guild_id TEXT,
      user_id TEXT,
      exp TEXT,
      lvl TEXT
    )
  ''')

  print("Bot is ready !")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))


@client.command()
async def hello(ctx):
    await ctx.send(f"Hello{ctx.message.author.mention}")

@client.command()
async def create(ctx, code, stime, duration):
    embed = discord.Embed(
        title="Forest",
        color = discord.Color.blue()
        )   
    try:
        if len(code) == 7 and len(stime) < 6 and len(duration) < 4:
          await ctx.send(discord.utils.get(ctx.guild.roles, name="Forest").mention)
          embed.add_field(name = "Hosted by: ", value = ctx.message.author.mention, inline = False)
          embed.add_field(name = "Code: ", value = code, inline = False)
          embed.add_field(name = "Starting Time: ", value = stime, inline = False)
          embed.add_field(name = "Duration: ", value = duration, inline = False)
          embed.add_field(name = "Link:", value = f"https://forestapp.cc/join-room?token={code}", inline = False)
          msg = await ctx.send(embed=embed)
          msg.add_reaction(":evergreen_tree:")

          user = await client.fetch_user(ctx.message.author.id)
          await DMChannel.send(user, f"Hello there, You have hosted a forest session at **{stime}** and code is **{code}** of **{duration}**mins")
          
        else:
          await ctx.send("The parameters which u have sent is not appropriate. Pls check it again")
    except:
        await ctx.send("Sorry, but give the full parameters required or type >help for the more commands")

@client.command()
async def ping(ctx):
    embed = discord.Embed(
        color= discord.Color.blue()
    )
    embed.add_field(name = "Ping", value= "Pong! {0}".format(round(client.latency, 1)), inline = False)

    await ctx.send(embed=embed)

@client.command()
async def welcome(ctx, channel:discord.TextChannel):
  if ctx.message.author.guild_permissions.manage_messages:
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is None:
      sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
      val = (ctx.guild.id, channel.id)
      await ctx.send(f"Channel has been set to {channel.mention}")
    elif result is not None:
      sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
      val = (channel.id,ctx.guild.id)
      await ctx.send(f"Channel has been updated to {channel.mention}")
    
    cursor.execute(sql,val)
    db.commit()
    cursor.close()
    db.close()

@client.event
async def on_message(message):
  if message.content.find("Time to put down your phone and get back to work! Enter my room code") != -1:
    await message.channel.send(f"Awww...please use me..pls {message.author.mention}")
  if client.user.mentioned_in(message):
    await message.channel.send(random.choice(cmds))
  db = sqlite3.connect('main.sqlite') 
  cursor = db.cursor()
  cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
  result = cursor.fetchone()
  await client.process_commands(message)
  if result is None:
    sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
    #compare user_id and val for the values u can change it
    val = (message.guild.id, message.author.id, 2, 0)
    cursor.execute(sql, val)
    db.commit()
  else:
    cursor.execute(f"SELECT user_id,exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
    result1 = cursor.fetchone()
    exp = int(result1[1])
    sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
    #val changes the exp value
    val = (exp + 2, str(message.guild.id), str(message.author.id))
    cursor.execute(sql,val)
    db.commit()
    

    cursor.execute(f"SELECT user_id,exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'")
    result2 = cursor.fetchone()

    xp_start = int(result2[1])
    lvl_start = int(result2[2])
    xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
    if xp_end < xp_start:
      await message.channel.send(f"{message.author.mention} Happy ? You levelled up to {lvl_start + 1}")
      sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
      val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
      cursor.execute(sql, val)
      db.commit()
      sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
      val = (0,str(message.guild.id), str(message.author.id))
      cursor.execute(sql, val)
      db.commit()
      cursor.close()
      db.close()


@client.command()
async def rank(ctx,user:discord.User=None):
  if user is not None:
    db = sqlite3.connect('main.sqlite') 
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}'")
    result = cursor.fetchone()
    if result is None:
      await ctx.send("Lmao he didnt started yet")
    else: 
      await ctx.send(f"Bruh, why do you want ? Anyaway {user.mention} he is currently level `{str(result[2])}` and has  `{str(result[1])}` XP")
    cursor.close()
    db.close()
  elif user is None:
    db = sqlite3.connect('main.sqlite') 
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
    result = cursor.fetchone()
    if result is None:
      await ctx.send("That user is not yet ranked")
    else:
      await ctx.send(f"{ctx.author.mention} is currently level `{str(result[2])}` and has  `{str(result[1])}` XP")
    cursor.close()
    db.close()   

@client.command()
async def top10(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, lvl, exp from levels WHERE guild_id = {ctx.guild.id} ORDER BY exp DESC LIMIT 5 ")
    result = cursor.fetchall()
    embed = discord.Embed(title="Leaderboards", colour=discord.Colour(0x6790a7))
    for i, x in enumerate(result, 1):
        embed.add_field(name=f"#{i}", value=f"<@{str(x[0])}> on Level {str(x[1])} with {str(x[2])} Total XP", inline=False)
    await ctx.send(embed=embed)
    print(result)
    cursor.close()
    db.close()
# @client.event
# async def on_member_join(member):
#     with open('users.json','r') as f:
#         users = json.load(f)

#     await update_data(users, member)

#     with open('users.json','w') as f:
#         json.dump(users,f)

# @client.event
# async def on_message(message):
#     with open('users.json','r') as f:
#         users = json.load(f)
    
#     await update_data(users, message.author)
#     await add_experience(users, message.author, 5)
#     await level_up(users, message.author, message.channel)

#     with open('users.json','w') as f:
#         json.dump(users,f)

#     await client.process_commands(message)

# async def update_data(users,user):
#   if not str(user.id) in users:
#       users[str(user.id)] = {}
#       users[str(user.id)]['experience'] = 0
#       users[str(user.id)]['level'] = 1
    
# async def add_experience(users, user, exp):
#   users[str(user.id)]['experience'] += exp

# async def level_up(users,user, channel):
#   experience = users[str(user.id)]['experience']
#   lvl_start = users[str(user.id)]['level']
#   lvl_end = int(experience ** (1/4))

#   if lvl_start < lvl_end:
#       await channel.send(f'GG!! {user.mention} u have leveled up to **{lvl_end}**!')
#       users[str(user.id)]['level'] = lvl_end

# @client.command()
# async def level(ctx, member: discord.Member = None):
#   if not member:
#     id = ctx.message.author.id
#     with open('users.json', 'r') as f:
#       users = json.load(f)
#       lvl = users[str(id)]['level']
#       await ctx.send(f'**{ctx.author.mention}** You are at level **{lvl}**!')
#   else:
#     id = member.id
#     with open('users.json', 'r') as f:
#       users = json.load(f)
#       lvl = users[str(id)]['level']
#       await ctx.send(f'{member.mention} is at level **{lvl}**!')

# def get_top_experience():
#   with open('users.json', 'r') as f:
#     users = json.load(f)
#   usersss = {}
#   for i in users.keys():
#     usersss[i] =  users[f'{i}']['experience']
#   rank = sorted(usersss, key=usersss.get, reverse=True)
#   return rank

# # @client.command()
# # async def rank(ctx):
# #   rank = get_top_experience()
# #   id = ctx.author.id
# #   num_rank = rank.index(str(id))
# #   await ctx.send(f'{ctx.author.mention} is at level {num_rank} and at rank')

# @client.command()
# async def rank(ctx, member: discord.Member = None):
#   rank = get_top_experience()
#   if not member:
#     id = ctx.author.id
#     with open('users.json', 'r') as f:
#       users = json.load(f)
#       lvl = users[str(id)]['level']
#       num_rank = rank.index(str(id))
#       await ctx.send(f'{ctx.author.mention} your rank is #**{num_rank + 1}**')
#   else:
#     id = member.id
#     with open('users.json', 'r') as f:
#       users = json.load(f)
#       lvl = users[str(id)]['level']
#       num_rank = rank.index(str(id))
#       await ctx.send(f'{member.mention} is and at rank is #**{num_rank + 1}**!')
@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount)

def sum(x,y):
  return int(x) + int(y)

@client.command()
async def add(ctx, num1, num2):
  sum = sum(int(num1), int(num2))
  try:
    await ctx.channel.send(f"{ctx.author.mention} The sum is {sum}")
  except:
    await ctx.channel.send(f"{ctx.author.mention} The format is <num1><num2>")
  
def diff(x,y):
  return int(x) - int(y)

@client.command()
async def subtract(ctx, num1, num2):
  diff = diff(int(num1), int(num2))
  try:
    await ctx.channel.send(f"{ctx.author.mention} The difference is {diff}")
  except:
    await ctx.channel.send(f"{ctx.author.mention} The format is <num1><num2>")

def product(x,y):
  return int(x) * int(y)

@client.command()
async def multiply(ctx, num1, num2):
  mult = product(int(num1), int(num2))
  try:
    await ctx.channel.send(f"{ctx.author.mention} The product is {mult}")
  except:
    await ctx.channel.send(f"{ctx.author.mention} The format is <num1><num2>")

def quotient(x,y):
  return int(x) / int(y)



@client.command()
async def div(ctx, num1, num2):
  div = quotient(int(num1), int(num2))
  try:
    await ctx.channel.send(f"{ctx.author.mention} The quotient is {div}")
  except:
    await ctx.channel.send(f"{ctx.author.mention} The format is <num1><num2>")
  
@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data    = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.id:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.id:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    



@client.command()
async def poll(ctx, *, message):
    emb = discord.Embed(title=" POLL", description=f"{message}")
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.id:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.id:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    
@client.command()
async def reactrole(ctx, emoji: discord.Emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji.id,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

@client.command(alias=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title=member.name, description=member.mention, color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id, inline=True)
    await ctx.send(embed=embed)

@client.command()
async def users(ctx):
    embed = discord.Embed(color=discord.Color.blue(), title=f"{ctx.guild.name}")
    embed.add_field(name="Total memebers in this server are ",value=f"{ctx.guild.member_count}")
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
  embed  = discord.Embed(title="Bot Help", colour=discord.Color.blue())
  embed.add_field(name="Forest", value = "Type >create {code} {starting time} {duration}. Dont include brackets", inline=False)
  embed.add_field(name="Hello", value="Type >hello, whenever u are feeling lonely", inline=False)
  embed.add_field(name="Rank", value="Type >rank to check ur rank, you can check ur friends rank too", inline=False)
  embed.add_field(name="ping", value="Type >ping to check ur ping", inline=False)
  embed.set_footer(icon_url=f"{ctx.guild.icon_url}", text=f"Server ID: {ctx.guild.id}")

  await ctx.send(embed=embed)
  

client.run('TOKEN')
