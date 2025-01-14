import discord, random, datetime
from discord.ext import tasks, commands
from cogs.economy import add_user_balance
from cogs.collectibles import check_counting_box, check_event_box

import secret
if secret.testBot:
    import testids as ids
else:
    import ids



def convert_to_num(message):

    result = ""

    for char in message.content:
        if char.isdigit():
            result = result + char

    if(result == ""):
        return None
    else:
        return int(result)



def sort_tally_table(table):
    n = len(table)

    for i in range(n):
        already_sorted = True

        for j in range (n - i - 1):
            if table[j][1] < table[j+1][1]:
                table[j], table[j+1] = table[j+1], table[j]
                already_sorted = False
        if already_sorted:
            break
    return table



class Count(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief="Shows the leaderboard of counts for the Count to 10,000.")
    async def tally(self, ctx):
        await ctx.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
        table = {}
        for count in reversed(history):
            if convert_to_num(count) == None:
                continue
            author = count.author
            if author in table.keys():
                table.update({author : table[author] + 1})
            else:
                table[author] = 1
        history = []
        counts = 0
        arrayTable = []
        for author in table:
            if author.id not in ids.blacklist:
                arrayTable.append([author.display_name, table[author]])
                counts += table[author]
        table = {}

        sortedTable = sort_tally_table(arrayTable)
        arrayTable = []

        tallyEmbed=discord.Embed(title="Count to 10,000", description=f"{counts} counts so far!", color=0xff5733)
        output = ""
        rank = 0
        displayRank = 0

        lastScore = 10000
        for author in sortedTable:
            rank += 1
            if author[1] < lastScore:
                displayRank = rank
                lastScore = author[1]
            output = output + f"{displayRank}: {author[0]} - {author[1]} \n"
        sortedTable = []

        tallyEmbed.add_field(name="Leaderboard", value=output, inline=False)

        await ctx.send("Done! Here's the data!")
        await ctx.send(embed=tallyEmbed)
        
    @commands.command(brief="Shows the messages over time for the Count to 10,000.")
    async def timeline(self, ctx):
        await ctx.send("Alright, working on it! There's a lot of data, so you might have to give me a couple of minutes..")
        history = await self.bot.get_channel(ids.channels["Count"]).history(limit=None).flatten()
        table = {}
        for count in history:
            if count.author.id not in ids.blacklist:
                pass
            else:
                time = count.created_at
                timeString = str(time.day) + "/" + str(time.month)
                if timeString in table.keys():
                    table.update({timeString : table[timeString] + 1})
                else:
                    table[timeString] = 1
        history = []
        counts = 0
        arrayTable = []
        for timeString in table:
            arrayTable.insert(0, [timeString, table[timeString]])
            counts += table[timeString]
        table = {}

        tallyEmbed=discord.Embed(title="Count to 6969", description=f"{counts} counts so far!", color=0xff5733)
        output1 = ""
        output2 = ""
        output3 = ""
        total = 0
        for time in arrayTable:
               output1 = output1 + time[0] + "\n"
               output2 = output2 + str(time[1]) + "\n"
               total += time[1]
               output3 = output3 + str(total) + "\n"
        arrayTable = []

        tallyEmbed.add_field(name="Date   ", value=output1, inline=True)
        tallyEmbed.add_field(name="Counts", value=output2, inline=True)
        tallyEmbed.add_field(name="Total", value=output3, inline=True)

        await ctx.send("Done! Here's the data!")
        await ctx.send(embed=tallyEmbed)

    async def get_last_count(self, message, limit):
        messageHistory = await message.channel.history(limit=limit).flatten()
        flag = False
        for pastMessage in messageHistory:
            if flag == False:
                if pastMessage.id == message.id:
                    flag = True
            else:
                if pastMessage.author.id not in ids.blacklist:
                    pastMessageValue = convert_to_num(pastMessage)
                    if pastMessageValue != None:
                        return pastMessage, pastMessageValue
        return message, messageValue

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == ids.channels["Count"] and message.author.id not in ids.blacklist:
            messageValue = convert_to_num(message)
            if messageValue != None:
                countCorrect = True
                lastMessage, lastMessageValue = await self.get_last_count(message, 5)

                diff = 0
                while lastMessage.reactions != []:
                    lastMessage, lastMessageValue = await self.get_last_count(lastMessage, 5)
                    diff += 1

                if message.author.id == lastMessage.author.id:
                    countCorrect = False
                    await message.add_reaction("❗")

                if messageValue != lastMessageValue + diff + 1:
                    countCorrect = False
                    await message.add_reaction("👀")

                if message.author.id in ids.mods:
                    timeStart = message.created_at
                    timeStart = timeStart - datetime.timedelta(minutes=9, seconds=timeStart.second)
                    tenMinHistory = await message.channel.history(limit=20, after=timeStart).flatten()
                    foundMessage = discord.utils.get(tenMinHistory, author = message.author)
                    if foundMessage != None and foundMessage != message:
                        countCorrect = False
                        await message.add_reaction("🕒")
                    
                if countCorrect == True:
                    add_user_balance(message.author.id, 1)
                    
                    eventbox = await check_event_box(message)
                    ##eventbox = False
                    if eventbox == False and random.randint(1,8) == 8:
                        await check_counting_box(message)

    @commands.Cog.listener()
    async def on_message_edit(self, oldMessage, message):
        if message.channel.id == ids.channels["Count"]:
            reactionsList = []
            for reaction in message.reactions:
                reactionsList.append(reaction.emoji)

            if '👀' in reactionsList:
                messageValue = convert_to_num(message)
                if messageValue != None:
                    lastMessage, lastMessageValue = await self.get_last_count(message, 20)

                    if messageValue == lastMessageValue + 1:
                        await message.add_reaction("🤩")

def setup(bot):
    bot.add_cog(Count(bot))
    print("Count Cog loaded")

def teardown(bot):
    print("Count Cog unloaded")
    bot.remove_cog(Count(bot))
