import discord
from discord.ext import tasks, commands
from asyncio import TimeoutError
from definitions import Member

import secret
if secret.testBot:
    import testids as ids
else:
    import ids

def add_user_balance(member_id, amount):
    member = Member.get(member_id)
    member.add_balance(amount)

def get_user_balance(member_id):
    member = Member.get(member_id)
    return member.get_balance()

class Economy(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="setbalance", aliases=["setbal"], brief="Sets the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def set_balance(self, ctx, target: discord.Member, amount: int):
        member = Member.get(target.id)
        member.set_balance(amount)
        await ctx.send(f"Set {target.display_name}'s balance to {amount}.")



    @commands.command(name="addbalance", aliases=["addbal", "addfunds"], brief="Adds to the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def add_balance(self, ctx, target: discord.Member, amount: int):
        member = Member.get(target.id)
        member.add_balance(amount)
        await ctx.send(f"{amount} added to {target.display_name}'s account.")



    @commands.command(name="getbalance", aliases=["getbal"], brief="Returns the target's SharkCoin balance.")
    @commands.has_role(ids.roles["Mod"])
    async def get_balance(self, ctx, target: discord.Member):
        member = Member.get(target.id)
        bal = member.get_balance()
        await ctx.send(f"{target.display_name}'s balance is: {bal}")



    @commands.command(aliases=["bal", "econ"], brief="Returns the user's SharkCoin balance.")
    async def balance(self, ctx):
        await ctx.invoke(self.bot.get_command("getbalance"), target = ctx.author)


    @commands.command(aliases=["transfer"])
    async def pay(self, ctx, target: discord.Member, amount: int):
        member = Member.get(ctx.author.id)
        targetMember = Member.get(target.id)
        if amount < 0:
            await ctx.send("Nice try buddy. Please enter a positive amount!")
            return


        if member.get_balance() < amount:
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
            member.add_balance(-amount)
            targetMember.add_balance(amount)
            await message.edit(content=f"Transferred {amount} to {target.display_name}.")
        else:
            await message.edit(content="Transfer cancelled.")
        






def setup(bot):
    bot.add_cog(Economy(bot))
    print("Economy Cog loaded")

def teardown(bot):
    print("Economy Cog unloaded")
    bot.remove_cog(Economy(bot))
