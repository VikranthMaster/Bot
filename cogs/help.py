import discord
from discord.ext import commands
import json
import asyncio
from discord.utils import get
from discord.ext.commands import command
from typing import Optional
from utils.util import Pag

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

  return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

client.remove_command("help")

# def syntax(command):
#     cmd_and_aliases = "|".join([str(command),*command.aliases])
#     params = []

#     for key, value in command.params.items():
#         if key not in ("self","ctx"):
#             params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
    
#     params = " ".join(params)
#     return f"```{cmd_and_aliases} {params}```"

# page1 = discord.Embed(title="**Bot help**",colour = discord.Color.blue())
# page1.add_field(name = "**Forest sessions**", value = f"For Forest sessions type ``>create (code) (starting time) (duration)``", inline=False)
# page1.add_field(name = "**ChangePrefix**", value = f"For Changing Prefix type ``>changeprefix (your new prefix)``", inline=False)
# page1.add_field(name = "**Fun**", value = f"Ping Sparta and get some nasty results", inline=False)
# page1.add_field(name = "**Clear Messages**", value = f"For clearing messages type ``>clear (amount of messages to be deleted)``", inline=False)
# page1.add_field(name = "**Poll**", value = f"To host a pll type ``>poll (your message)``", inline=False)


# page2 = discord.Embed(title="**Bot help**",colour = discord.Color.blue())
# page2.add_field(name = "**TicTacToe**", value = f"Fpr playing tictactoe Type ``>tictactoe (player1 mention) (player2 mention)``", inline=False)
# page2.add_field(name = "**Memes**", value = f"For Funny memes type ``>meme``", inline=False)
# page2.add_field(name = "**Gifs**", value = f"To get some gifs type ``>gif (your Genre)``", inline=False)
# page2.add_field(name = "**Quotes**", value = f"To get some nice quotes type ``>quote``", inline=False)
# page2.add_field(name = "**Gifs**", value = f"To get some gifs type ``>gif (your Genre)``", inline=False)


# page3 = discord.Embed(title="**Bot help**",colour = discord.Color.blue())
# page3.add_field(name = "**Music**", value = f"For listening to music Type ``>join`` then ``>play (your favourite song url)`` and for adding it to queue type ``>queue (url)``", inline =False)
# page3.add_field(name="**DM**", value = f"For Dming a user type ``>dm (user)``")
# page3.add_field(name="**Maths**", value = f"For doing maths you can type ``>add (num1) (num2)`` or ``>subtract (num1) (num2)`` or ``>multiply (num1) (num2)`` or ``>divide (num1) (num2)``")
# page3.add_field(name="****", value = f"For Dming a user type ``>dm (user)``")

# page4 = discord.Embed(title="**Bot help**", color = discord.Color.blue())
# page4.add_field(name="**Rank**", value = f"To check your rank type ``>rank``")
# page4.add_field(name="**Leaderboard**", value = f"To check leaderboard type ``>leaderboard``")
# page4.add_field(name="**Question**", value = f"If you want to play with sparta simply time ``>q (anything you want to type)``")

# client.help_pages = [page1, page2, page3, page4]

# class Help(commands.Cog):
#     def __init__(self, client):
#         self.client = client
    
#     @commands.Cog.listener()
#     async def on_ready(self):
#         print("Help cog is loaded !")

#     @commands.command()
#     async def help(self,ctx):
#         buttons = [u"\u23EA",u"\u25C0",u"\u25B6",u"\u23E9"]
#         current = 0
#         msg = await ctx.send(embed = client.help_pages[current])

#         for button in buttons:
#             await msg.add_reaction(button)
  
#         while True:
#             try:
#                 reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user : user == ctx.author and reaction.emoji in buttons, timeout=60.0)
            
#             except asyncio.TimeoutError:
#                 embed = client.help_pages[current]
#                 embed.set_footer(text="Timed Out.")
#                 await msg.clear_reactions()

#             else:
#                 previous_page = current

#             if reaction.emoji == u"\u23EA":
#                 current = 0

#             elif reaction.emoji == u"\u25C0":
#                 if current > 0:
#                     current -= 1
            
#             elif reaction.emoji == u"\u25B6":
#                 if current < len(client.help_pages)-1:
#                     current += 1
                
#             elif reaction.emoji == u"\u23E9":
#                 current = len(client.help_pages)-1
            
#             for button in buttons:
#                 await msg.remove_reaction(button, ctx.author)
            
#             if current != previous_page:
#                 await msg.edit(embed=client.help_pages[current])
    
    # async def cmd_help(self, ctx, command):
    #     embed = Embed(title=f"Help With ``{command}`` ", description=syntax(command), color=discord.Color.blue())
    #     embed.add_field(name = "Command Description", value = command.help)
    #     await ctx.send(embed=embed)

    # @commands.command
    # async def help(self,ctx, cmd : Optional[str]):
    #     if cmd is None:
    #         pass
    #     else:
    #         if (command := get(self.client.commands, name=cmd)):
    #             await self.cmd_help(ctx, command)
    #         else:
    #             await ctx.send("That command does not exist")

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cmds_per_page = 6
    
    def get_command_signature(self, command : commands.Command, ctx : commands.Context):
        aliases= "|".join(command.aliases)
        cmd_invoke = f"[{command.name} {aliases}]" if command.aliases else command.name

        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    async def return_filtered_commands(self,walkable,ctx):
        filtered = []

        for c in walkable.walk_commands():
            try:
                if c.hidden:
                    continue
                elif c.parent:
                    continue
                await c.can_run(ctx)
                filtered.append(c)
            except commands.CommandError:
                continue
        return self.return_sorted_commands(filtered)
    
    def return_sorted_commands(self,commandList):
        return sorted(commandList, key=lambda x: x.name)

    async def setup_help_pag(self,ctx,entity=None,title=None):
        entity = entity or self.client
        title = title or self.client.description

        pages = []

        if isinstance(entity, commands.Command):
            filtered_commands = (
                list(set(entity.all_commands.values()))
                if hasattr(entity, "all_commands")
                else []
            )

        else:
            filtered_commands = await self.return_filtered_commands(entity,ctx)
        
        for i in range(0, len(filtered_commands),self.cmds_per_page):
            next_commands = filtered_commands[i : i+ self.cmds_per_page]
            commands_entry = ""

            for cmd in next_commands:
                desc = cmd.short_doc or cmd.description
                signature = self.get_command_signature(cmd,ctx)
                subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

                commands_entry += (
                    f" . **__{cmd.name}__**\n```\n{signature}\n ```\n{desc}\n"
                    if isinstance(entity, commands.Command)
                    else f". **__{cmd.name}__**\n{desc}\n    {subcommand}\n"
                )
            pages.append(commands_entry)
        await Pag(title=title, color=discord.Color.blue(), entries=pages, length=1).start(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Cog loaded")
    
    @commands.command(name="help", aliases=["h","commands"])
    async def help_commands(self, ctx, *, entity=None):
        if not entity:
            await self.setup_help_pag(ctx)


def setup(client):
    client.add_cog(Help(client))
