import discord
from discord.ext import commands
from discord import DMChannel
import os
import json
import asyncio

client = commands.Bot(command_prefix=">")
os.chdir(r"C:\Users\shankar\Desktop\python\music")

@client.event
async def on_ready():
    print("Bot is ready !")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))


@client.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.message.author.mention}")

@client.command()
async def create(ctx, stime, code, duration):
    embed = discord.Embed(
        title="Forest",
        color = discord.Color.blue()
    )   
    try:
        embed.add_field(name = "Hosted by: ", value = ctx.message.author.mention, inline = False)
        embed.add_field(name = "Code: ", value = code, inline = False)
        embed.add_field(name = "Starting Time: ", value = stime, inline = False)
        embed.add_field(name = "Duration: ", value = duration, inline = False)

        await ctx.send(embed=embed)

        user = await client.fetch_user(ctx.message.author.id)
        await DMChannel.send(user, "Hello there!, you have hosted a forest session at" + (stime) + "and code is " + (code))

    except:
        await ctx.send("Sorry, but give the full parameters required or type >help for the more commands")

@client.command()
async def ping(ctx):
    embed = discord.Embed(
        color= discord.Color.blue()
    )
    embed.add_field(name = "Ping", value= "Pong! {0}".format(round(client.latency, 1)), inline = False)

    await ctx.send(embed=embed)

@client.event
async def on_member_join(member):
    with open('users.json','r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json','w') as f:
        json.dump(users,f)

@client.event
async def on_message(message):
    with open('users.json','r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json','w') as f:
        json.dump(users,f)

async def update_data(users,user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1
    
async def add_experience(users, user, exp):
    users[str(user.id)]['experience'] += exp

async def level_up(users,user, channel):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await channel.send(f'GG! {user.mention} you have levelled up to {lvl_end}')
        users[str(user.id)]['level'] = lvl_end
