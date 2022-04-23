import json
import discord
from discord.ext import tasks, commands

import secret
if secret.testBot:
	import testids as ids
else:
	import ids

mapDict = {
        "a": "Ascent",
        "bi": "Bind",
        "br": "Breeze",
        "f": "Fracture",
        "h": "Haven",
        "i": "Icebox",
        "s": "Split"
}

	
	
class Valorant(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		 		
	
	def load_file(self, fileName, canCreate):
		try:
			with open(f"data/valorant/{fileName}.json", "r") as infile:
				return json.load(infile)
		except FileNotFoundError:
			if canCreate == True:
				createFile = open(f"data/valorant/{fileName}.json", "w")
				createFile.write("{}")
				createFile.close()
			return {}
		
	async def save_file(self, ctx, data):
		with open("data/valorant/userdata.json", "w") as outfile:
			json.dump(data, outfile, indent=4)
		await ctx.send("List has been updated.")

	async def help_comm(self, ctx):
		helpEmbed = discord.Embed(title="Valorant Commands", color=0x660000)
		commList = ""
		commList = commList + f"$v show <user> <map> - Shows the user's agent list for this map. \n"
		commList = commList + f"$v update <user> <map> <agent list> - Replaces the user's list of played agents for this map. \n"
		commList = commList + f"$v add <user> <map> <agent list> - Adds the list of agents to the user's played agents for this map. \n"
		commList = commList + f"$v remove <user> <map> <agent list> - Removes the list of agents from the user's played agents for this map. \n"
		commList = commList + f"$v new <map> <user1> <user2> <user3> <user4> <user5> - Replaces map session with a new one and gives initial insight. \n"
		commList = commList + f"$v lock <user> <agent> - Updates current map session information using newly locked in agent. \n"
		helpEmbed.add_field(name="Command List", value=commList, inline=False)
		await ctx.send(embed=helpEmbed)
	

	
	async def show_comm(self, ctx, target, mapName):
		data = self.load_file("userdata", True)
		if target in data:
                        if mapName in data[target]:
                                await ctx.send(data[target][mapName])
                        else:
                                await ctx.send("User has no agents registered for this map. Try adding them with $v add <user> <map> <agents>")
		else:
			await ctx.send("User has no agents registered for this map. Try adding them with $v add <user> <map> <agents>")
      		
		
	async def update_comm(self, ctx, target, mapName, *agents):
                if len(mapName) > 2:
                        mapName = mapName[:2]
                if mapName[0] in ["a", "f", "h", "i", "s"]:
                        mapName = mapName[0]
                try:
                        mapName = mapDict[mapName]
                except KeyError:
                        await ctx.send("Could not determine intended map.")
                        return
                data = self.load_file("userdata", True)
                data[target] = {}
                data[target][mapName] = agents
                await self.save_file(ctx, data)
		
      		
		
	async def add_comm(self, ctx, target, mapName, *agents):
		data = self.load_file("userdata", True)
		for item in agents:
			if item not in data[target][mapName]:
				data[target][mapName].append(item)
		await self.save_file(ctx, data)
		
      		
		
	async def remove_comm(self, ctx, target, mapName, *agents):
		data = self.load_file("userdata", True)
		for item in agents:
			if item in data[target][mapName]:
				data[target][mapName].remove(item)
		await self.save_file(ctx, data)
      		
	
	async def new_comm(ctx, mapName, target1, target2, target3, target4, target5):
		mapData = load_file(f"{mapName}data", False)
		if target1 == None:
			party = 0				 
		elif target2 == None:
			party = 1				 
		elif target3 == None:
			party = 2
		elif target4 == None:
			party = 3
		elif target5 == None:
			party = 4
		else:
			party = 5
							 
		if party != 0:
			ctx.send("Cheese!")
			
		
      		
	
	async def lock_comm(ctx, target, agentName):
		await ctx.send("Command not found. Try $v to get started.")
      		
    
	@commands.command(name="valorant", aliases=["val", "v"], brief="Default Valorant command.")
	async def val_comm(self, ctx, *args):
		if args == ():
			await self.help_comm(ctx)
		elif args[0] in ["show", "s", "agents", "agent", "a"] and len(args) == 3:
			await self.show_comm(ctx, args[1], args[2])
		elif args[0] in ["update", "u", "replace", "rep"] and len(args) > 3:
      			await self.update_comm(ctx, args[1], args[2], args[3:])
		elif args[0] == "add":
      			await self.add_comm(ctx, args[1], args[2], args[3])
		elif args[0] in ["remove", "rem"]:
      			await self.remove_comm(ctx, args[1], args[2], args[3])
		elif args[0] in ["new", "n", "game", "g", "map", "m"]:
      			await self.new_comm(ctx, args[1], args[2], args[3], args[4], args[5], args[6])
		elif args[0] in ["locked", "lock", "l", "picked", "picks", "pick", "p"]:
      			await self.lock_comm(ctx, args[1], args[2])
		else:
			await self.help_comm(ctx)
		
		
		
def setup(bot):
	bot.add_cog(Valorant(bot))
	print("Valorant Cog loaded")

def teardown(bot):
	print("Valorant Cog unloaded")
	bot.remove_cog(Valorant(bot))