import discord
from discord.ext import tasks, commands
from asyncio import TimeoutError

import secret
if secret.testBot:
    import testids as ids
else:
    import ids
    


def read_econ():
    r = open("econ.txt", "r")
    fileData = r.read()
    r.close()

    split1 = fileData.split(";")
    split2 = {}
    for item in split1:
        split = item.split(":")
        split2[int(split[0])] = int(split[1])

    return split2



def write_econ(data):
    fileData = ""
    for account in data:
        fileData = fileData + f"{int(account)}:{int(data[account])};"
    fileData = fileData[:-1]

    w = open("econ.txt", "w")
    w.write(fileData)
    w.close()



def get_user_balance(id):
    data = read_econ()
    try:
        return data[id]
    except:
        data[id] = 0
        write_econ(data)
        return data[id]



def set_user_balance(id, balance):
    data = read_econ()
    data[id] = balance
    write_econ(data)



def add_user_balance(id, amount):
    data = read_econ()
    try:
        data[id] = data[id] + amount
    except KeyError:
        data[id] = amount
    write_econ(data)


class Economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="setbalance", aliases=["setbal"], brief="Sets the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def set_balance(self, ctx, target: discord.Member, amount: int):

        set_user_balance(target.id, amount)
        await ctx.send(f"Set {target.display_name}'s balance to {amount}.")



    @commands.command(name="addbalance", aliases=["addbal", "addfunds"], brief="Adds to the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def add_balance(self, ctx, target: discord.Member, amount: int):

        add_user_balance(target.id, amount)
        await ctx.send(f"{amount} added to {target.display_name}'s account.")



    @commands.command(name="getbalance", aliases=["getbal"], brief="Returns the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def get_balance(self, ctx, target: discord.Member):

        bal = get_user_balance(target.id)
        await ctx.send(f"{target.display_name}'s balance is: {bal}")



    @commands.command(aliases=["bal", "econ"], brief="Returns the user's SharkCoin balance.")
    async def balance(self, ctx):
        await ctx.invoke(self.bot.get_command("getbalance"), target = ctx.author)


    @commands.command(aliases=["transfer"])
    async def pay(self, ctx, target: discord.Member, amount: int):
        if amount < 0:
            await ctx.send("Nice try buddy. Please enter a positive amount!")
            return


        if get_user_balance(ctx.author.id) < amount:
            await ctx.send("Sorry, you don't have enough coins to do that.")
            return

        message = await ctx.send(f"Transfer {amount} to {target.display_name}?")
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        check = lambda reaction, user: user == ctx.author and reaction.message == message and reaction.emoji in ["✅", "❌"]

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except TimeoutError:
            await message.edit(content="Transfer cancelled, timed out.")
            return

        if reaction.emoji == "✅":
            add_user_balance(ctx.author.id, -amount)
            add_user_balance(target.id, amount)
            await message.edit(content=f"Transferred {amount} to {target.display_name}.")
        else:
            await message.edit(content="Transfer cancelled.")
        






def setup(bot):
    bot.add_cog(Economy(bot))
    print("Economy Cog loaded")

def teardown(bot):
    print("Economy Cog unloaded")
    bot.remove_cog(Economy(bot))
