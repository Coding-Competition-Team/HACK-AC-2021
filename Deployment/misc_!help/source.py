import discord
import logging
import asyncio
import os
from discord.ext import commands
logging.basicConfig(level=logging.INFO)
bot_token=os.getenv("BOT_TOKEN")
client = commands.Bot(command_prefix="!", case_insensitive=True, description="Hello! I'm a multi-purpose bot with many functionalities.")

@client.event
async def on_ready():
    print("ready")

@client.check
async def check(ctx):
    return not ctx.message.guild

@client.command(brief="Free flags!!", description="Free flag generator for all your CTF needs!", usage="1337fl4g")
async def flag(ctx, *args):
    if not args:
        await ctx.channel.send("```\nWhat flag you want sia, need to specify\n```")
        return
    arg = args[0]
    await ctx.channel.trigger_typing()
    await ctx.send("```\nHere's your flag!!!!\n```")
    await ctx.send("```\nACSI{%s}\n```" % arg)

@client.command(brief="Pick any image from our database.", description="To use this command, run the command with the argument as the image you want to view.", usage="image1.png")
async def image(ctx, *args):
    if not args:
        await ctx.channel.send("```\nYou need to specify an image\n```")
        return
    await ctx.channel.trigger_typing()
    arg = args[0]
    if arg != "image0.png" and arg != "image1.png" and arg != "image2.png" and arg != "image3.png":
        await ctx.send("```\nSorry, image not found. :(\n```")
    else:
        f = discord.File("/app/files/" + arg)
        await ctx.send("```\nHere you go!\n```", file=f)

@client.command(brief = "Upload zip files here!", description="Upload any zip file to our database, and I'll echo its contents back to you.", usage="(with zip file attached)")
async def upload(ctx):
    if not ctx.message.attachments:
        await ctx.send("```\nYou need to actually attach a file\n```")
        return
    try:
        await ctx.channel.trigger_typing()
        await ctx.message.attachments[0].save("file.zip")
        os.system("unzip file.zip -d temp")
        os.system("cat temp/* > out.txt")
        os.system("rm -rf temp && rm file.zip")
        with open("out.txt") as f:
                out = f.read()
        await ctx.send("```\n%s\n```" % out)
        os.system("rm out.txt")
    except:
        os.system("rm file.zip")
        os.system("rm -rf temp")
        os.system("rm out.txt")
        await ctx.send("```\nSorry, something went wrong. :(\n```")

@client.command(brief="Pings the bot.", description="Pings the bot.")
async def ping(ctx):
    await ctx.channel.trigger_typing()
    os.system("touch ping.txt")
    os.system("ping -c 5 0 >> ping.txt")
    with open("ping.txt") as f:
        ping = f.read()
    await ctx.send("```\n%s\n```" % ping)
    os.system("rm ping.txt")

@client.command(brief="Reacts to the last 20 messages.", description="Reacts to the last 20 messages.")
async def react(ctx):
    await ctx.send("```\nuh ok\n```")
    async for m in ctx.channel.history(limit=20):
        await m.add_reaction("\N{Confounded Face}")
    await ctx.send("```\nDone\n```")

@client.command(brief="Hangman!", description="Hangman! The word isn't \"Flag\" btw.")
async def hangman(ctx):
    await ctx.send("```\n_ _ _ _\n```")
    await ctx.send("```\nYou have 1 guess left.\n```")
    await client.wait_for("message", timeout=10.0)
    await ctx.send("```\nnvm git gud\n```")

@client.command(brief="Tic tac toe.", description="Tic tac toe is fun, isn't it? To claim a square, do A1, B2 etc.")
async def tictactoe(ctx):
    await ctx.send("░ ░ ░\n░ ░ ░\n░ ░ ░")
    await ctx.send("```\nYour turn!\n```")
    try:
        msg = await client.wait_for("message", timeout=10.0)
    except:
        await ctx.send("░ ░ ░\n░ ░ ░\n░ ░ ░")
        await ctx.send("```\nYou lose\n```")
        return
    if msg.content == "A1":
        await ctx.send("█ ░ ░\n░ ░ ░\n░ ░ ░")
    elif msg.content == "A2":
        await ctx.send("░ █ ░\n░ ░ ░\n░ ░ ░")
    elif msg.content == "A3":
        await ctx.send("░ ░ █\n░ ░ ░\n░ ░ ░")
    elif msg.content == "B1":
        await ctx.send("░ ░ ░\n█ ░ ░\n░ ░ ░")
    elif msg.content == "B2":
        await ctx.send("░ ░ ░\n░ █ ░\n░ ░ ░")
    elif msg.content == "B3":
        await ctx.send("░ ░ ░\n░ ░ █\n░ ░ ░")
    elif msg.content == "C1":
        await ctx.send("░ ░ ░\n░ ░ ░\n█ ░ ░")
    elif msg.content == "C2":
        await ctx.send("░ ░ ░\n░ ░ ░\n░ █ ░")
    elif msg.content == "C3":
        await ctx.send("░ ░ ░\n░ ░ ░\n░ ░ █")
    elif "flag" in msg.content:
        await ctx.send("█ █ █ ░ █ ░ ░ ░ ░ █ ░ ░ ░ █ █\n█ ░ ░ ░ █ ░ ░ ░ █ ░ █ ░ █ ░ ░\n█ █ ░ ░ █ ░ ░ ░ █ █ █ ░ █ █ █\n█ ░ ░ ░ █ ░ ░ ░ █ ░ █ ░ █ ░ █\n█ ░ ░ ░ █ █ █ ░ █ ░ █ ░ ░ █ ░")
    else:
        await ctx.send("```Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in ACSI{fake_flag} in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n```")
    await ctx.channel.trigger_typing()
    await asyncio.sleep(3)
    await ctx.send("█ █ █\n█ █ █\n█ █ █")
    await ctx.send("```\nYou Win!\n```")


client.run(bot_token)
    
