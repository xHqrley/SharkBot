import discord
from discord.ext import commands

import sys
import os
import datetime

import secret



bot = commands.Bot("$")



if secret.testBot:
    import testids as ids
else:
    import ids



@bot.event
async def on_ready():
    os.system("git pull")
    print(f"Sharkbot ready on {bot.user} : {bot.user.id}")
    chaos = await bot.fetch_user(ids.users["Chaos"])    
    
    await chaos.send("SharkBot is up and running!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="nom nom nom!"))
    
    r = open("reboot.txt", "r")
    replyTxt = r.read()
    replyFlag, replyID = replyTxt.split()
    r.close()
    
    if replyFlag == "True":
        replyChannel = await bot.fetch_channel(int(replyID))
        await replyChannel.send("I'm back!")
        w = open("reboot.txt", "w")
        w.write(f"False {replyID}")
        w.close()
    
    print("")
    print("The bot is currently in these servers:")

    for guild in bot.guilds:
        print(f"{guild.name} : {guild.id}")



@bot.command()
@commands.check_any(commands.is_owner())
async def reboot(message):
    if message.author.id != ids.users["Chaos"]:
        await message.channel.send("I'm afraid you're not allowed to do that!")
    else:
        await message.channel.send("Alright! Rebooting now!")
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="I'm just rebooting!"))
        
        f = open("reboot.txt", "w")
        f.write("True " + str(message.channel.id))
        f.close()

        os.system("sudo reboot")



@bot.command()
@commands.check_any(commands.is_owner())
async def load(message, extension):
    bot.load_extension(f"cogs.{extension.lower()}")
    await message.channel.send(f"{extension.capitalize()} loaded.")


    
@bot.command()
@commands.check_any(commands.is_owner())
async def unload(message, extension):
    bot.unload_extension(f"cogs.{extension.lower()}")
    await message.channel.send(f"{extension.capitalize()} unloaded.")


    
@bot.command()
@commands.check_any(commands.is_owner())
async def reload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} reloaded.")
    print(f"{extension.capitalize()} Cog reloaded.")



@bot.command()
@commands.check_any(commands.is_owner())
async def rebuild(ctx, extension = "all"):
    await ctx.invoke(bot.get_command("pull"))
    extension = extension.lower()
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension.capitalize()} reloaded.")
    print(f"{extension.capitalize()} Cog reloaded.")



@bot.command()
@commands.check_any(commands.is_owner())
async def pull(ctx):
    os.system("git pull")
    await ctx.send("Pulling latest commits.")




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't know that command!")
        return
    if isinstance(error, commands.CheckAnyFailure):
        await ctx.send("Sorry, you can't do that!")
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("I think you're missing an argument there!")
        return
    raise error



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")



bot.run(secret.token)
