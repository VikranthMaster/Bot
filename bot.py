import discord
from discord.ext import commands, timers
from discord.utils import get
from discord import DMChannel
import os
import asyncio
import sqlite3
import math 
import random
import time
import datetime
import requests
import youtube_dl
import aiohttp
import json
import shutil
from os import system


player1 = ""
player2 = ""
turn = ""
gameOver = True

#implement "if message.author != client.user" in exp system

board = []

api_key = "5e74111393bae2a5c24675da1604b841"

cmds = ["Duh, Stop talking to me and get back to work.","Who the hell summoned me?! I am sleeping !!","Bruh, what do you want ?!","Hey sorry i was so mean !", "Heya whats up ?", "Hey handsome !", "Yo! Dude sup"]
hello = ["hello","hi","hey","Hello","Hi","Hey"]

client = commands.Bot(command_prefix = ">",intents=discord.Intents.all())

command_prefix = "w."

client.remove_command("help")

@client.event
async def on_ready():
  db = sqlite3.connect('test.sqlite')
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

  db = sqlite3.connect("forest.sqlite")
  cursor = db.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS forest(
      guild_id TEXT,
      user_id TEXT,
      points TEXT
    )
  ''')
  print("Database loaded")
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
    db = sqlite3.connect('test.sqlite')
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

@client.event
async def on_message(message):
  if message.content.find("Time to put down your phone and get back to work! Enter my room code") != -1:
    await message.channel.send(f"Awww...please use me..pls {message.author.mention}")
  if client.user.mentioned_in(message):
    await message.channel.send(random.choice(cmds))
  if message.author != client.user and message.content.startswith(command_prefix):
    location = message.content.replace("w.", "").lower()
    if len(location) >= 1:
      url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
      try:
        data = json.loads(requests.get(url).content)
        data = parse_data(data)
        await message.channel.send(embed=weather_message(data, location))
      except KeyError:
        await message.channel.send(embed=error_message(location))
  remove = message.content.replace(">play", "").lower()
  


  db = sqlite3.connect('test.sqlite') 
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
    db = sqlite3.connect('test.sqlite') 
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
    db = sqlite3.connect('test.sqlite') 
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.guild.id}' and user_id = '{ctx.author.id}'")
    result = cursor.fetchone()
    if result is None:
      await ctx.send("You didnt start lmao")
    else:
      await ctx.send(f"{ctx.author.mention} are currently level `{str(result[2])}` and have  `{str(result[1])}` XP")
    cursor.close()
    db.close()   

@client.command()
async def leaderboard(ctx):
    db = sqlite3.connect('test.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, lvl, exp from levels WHERE guild_id = {ctx.guild.id} ORDER BY lvl and exp DESC LIMIT 5 ")
    result = cursor.fetchall()
    embed = discord.Embed(title="Leaderboards", colour=discord.Colour.blue())
    for i, x in enumerate(result, 1):
      embed.add_field(name=f"#{i}", value=f"<@{str(x[0])}> on Level {str(x[1])} with {str(x[2])} Total XP", inline=False)
    await ctx.send(embed=embed)
    cursor.close()
    db.close()

@client.command()
async def level(ctx):
  db =sqlite3.connect("test.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT user_id, lvl from levels WHERE guild_id = {ctx.guild.id} and user_id = {ctx.user.id}")
  result = cursor.fetchone()
  if result is None:
    await ctx.send("User didnt start")
  else:
    await ctx.send(f"{ctx.author.mention} you are on Level **{str(result[1])}**")
  cursor.close()
  db.close()

@client.command()
async def xp(ctx):
  db = sqlite3.connect("test.sqlite")
  cursor = db.cursor()
  cursor.execute(f"SELECT user_id, exp from levels WHERE guild_id = {ctx.guild.id} and user_id = {ctx.user.id}")
  result = cursor.fetchone()
  if result is None:
    await ctx.send("User not started")
  else:
    await ctx.send(f"{ctx.author.mention} your current XP is **{str(result[0])}**")
  cursor.close()
  db.close()


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
                    

@client.command()
async def poll(ctx, *, message):
    emb = discord.Embed(title=" POLL", description=f"{message}")
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


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
async def dm(ctx, member:discord.Member):
  await ctx.send("what do you want to say")
  def check(msg):
    return msg.author.id == ctx.message.author.id

  message = await client.wait_for('message',check=check)
  await ctx.send(f'sent message to {member.mention}')

  await member.send(f'{ctx.author.mention} Has a message for you:\n {message.content}')


@client.command()
async def quote(ctx):
  results = requests.get("https://type.fit/api/quotes/").json()
  num = random.randint(1,1500)
  content = results[num]["text"]
  embed = discord.Embed(color= discord.Color.blue())
  embed.add_field(name="Quote:", value=f"*{content}*")

  await ctx.send(embed=embed)

@client.command(pass_context=True)
async def meme(ctx):
  embed = discord.Embed(color=discord.Color.blue())

  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
      res = await r.json()
      embed.set_image(url=res['data']['children'] [random.randint(0, 100)]['data']['url'])
      await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
  
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          print("Downloading audio now\n")
          ydl.download([url])
    except:
      print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
      c_path = os.path.dirname(os.path.realpath(__file__))

      # remove = ctx.replace(">play","").lower()
      # system(f"spotdl {remove}")
      


    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
      shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


queues = {}

@client.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")

@client.command(pass_context=True, aliases=['skip'])
async def next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing next song")
        voice.stop()
        await ctx.send("PLaying next song")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing")



player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos : int):
  global turn
  global player1
  global player2
  global board
  global count

  if not gameOver:
    mark = ""
    if turn == ctx.author:
      if turn == player1:
        mark = ":o2:"
      elif turn == player2:
        mark = ":regional_indicator_x:"
      
      if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
        board[pos - 1] = mark
        count += 1

        line = ""
        for x in range(len(board)):
          if x == 2 or x == 5 or x == 8:
            line += " " + board[x]
            await ctx.send(line)
            line = ""
          else:
            line += " " + board[x]
        
        checkWinner(winningConditions, mark)
        if gameOver:
          await ctx.send(f"{mark} wins!")
        elif count >= 9:
          await ctx.send("Its a tie!")

        if turn == player1:
          turn = player2
        elif turn == player2:
          turn = player1

      else:
        await ctx.send("**Lmao that space has been taken by your opponent**")
    else:
      await ctx.send("It is not your turn.")
  else:
    await ctx.send("Please start a new game using >tictactoe command.")

def checkWinner(winningConditions, mark):
  global gameOver
  for condition in winningConditions:
    if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
      gameOver = True

@tictactoe.error
async def tictactoe_error(ctx,error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please mention 2 players for this game.")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Please make sure to mention/ping players")



@place.error
async def place_error(ctx,error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please mention a position to mark")
  elif isinstance(error, commands.BadArgument):
    await ctx.send("Please make sure it is an integer")

@client.command()
async def test(ctx):
  width = 9
  height = 9
  grid = ""
  i = int(0)
  for i in range(width):
    grid+=(":white_large_square:")
  for i in range(height):
    await ctx.send(grid)
  
  


@client.command()
async def help(ctx):
  embed  = discord.Embed(title="Bot Help", colour=discord.Color.blue())
  embed.add_field(name="Forest", value = "Type >create {code} {starting time} {duration}. Dont include brackets", inline=False)
  embed.add_field(name="Hello", value="Type >hello, whenever u are feeling lonely", inline=False)
  embed.add_field(name="Rank", value="Type >rank to check ur rank, you can check ur friends rank too", inline=False)
  embed.add_field(name="ping", value="Type >ping to check ur ping", inline=False)
  embed.set_footer(icon_url=f"{ctx.guild.icon_url}", text=f"Server ID: {ctx.guild.id}")

  await ctx.send(embed=embed)
  

client.run("TOKEN")

