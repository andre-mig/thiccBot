#thiccBot.py

import os 
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD1')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# async def Author_Responses(message, num):

#     response = ""
#     if str(message.author) == "scoot#6332" and num <= 10:
#         if num < 7:
#             response = "You should tell your girlfriend she's pretty more often."
#         else:
#             response = "Shut the fuck up, scoot."

#     elif str(message.author) == "waverly ✵☽#0994" and num <= 5:
#         response = "wil ur a plat"

#     elif str(message.author) == "Miggy#7541" and num <=3:
#         response = "I love you dad"

#     elif str(message.author) == "Tomz117#0624" and num <= 20:
#         response = ""

#     elif str(message.author) == "Dumpy#7108" and num <= 7:
#         response = "💧🍑💧"

#     elif str(message.author) == "Hayden#9935" and num <= 10:
#         response = "🍌"

#     elif str(message.author) == "BroBrownie#2354" and num <= 7:
#         if num <= 3:
#             response = "Just so you know, Anime girls don't count."
#         else:
#             response = "You will never have an RLGF"

#     elif str(message.author) == "jacques#1431" and num <= 10:
#         if num < 5:
#             response = "Ok Jack"
#         else:
#             response = "Ok Jock"

#     elif str(message.author) =="PenguinWithPants#2781" and num <= 10:
#         response = "weeb shit"

#     elif num > 98:
#         response = "Shut the fuck up, scoot."

#     if response != "":
#         await message.channel.send(response)

async def Message_Contains_Responses(message):
    msg = str(message.content).lower()
    if 'thiccbot' in msg or 'thiccbot' in str(message.mentions).lower():
        await message.channel.send("I'm back bitches.")


class Player:
    name = ""
    wins = 0
    losses = 0
    goalsFor = 0
    goalsAgainst = 0
    placement = 0
    def __init__(self,name):
        self.name = name

class Mixup:
    numGamesPlayed = 0
    scheduleArr = [
        [1,2,3,4], [1,2,4,5], [1,2,3,5],
        [1,3,2,4], [1,3,2,5], [1,3,4,5],
        [1,4,2,3], [1,4,2,5], [1,4,3,5],
        [1,5,2,3], [1,5,2,4], [1,5,3,4],
        [2,3,4,5], [2,4,3,5], [2,5,3,4]
    ]
    scheduleArr4 = [
        [1,2,3,4], [1,3,2,4], [1,4,2,3],
        [1,2,3,4], [1,3,2,4], [1,4,2,3],
        [1,2,3,4], [1,3,2,4], [1,4,2,3]
    ]
    randSchedule = scheduleArr
    randSchedule4 = scheduleArr4

mixup = Mixup()
playerArr = []

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await Message_Contains_Responses(message)

@bot.command()
async def botHelp(ctx):
    messageArr = [
        "I have now been turned in to a mixup logistics bot. I probably won't give you all as much shit unfortunately. You can now use me to setup a 5-player 2v2 mixup.",
        "First, send the command '!setup' with a list of your players' names. Example: '!setup p1 p2 p3 p4 p5'. I'll randomly generate a schedule and keep score. Once I'm done setting it up, I'll send you the first game.",
        "After each game, send me the score with '!result' in the order I gave you the teams.",
        "For example, if the game I gave you was 'player1, player2 vs. player3, player4' and players 1 and 2 won the game, you would send: '!score 2 1', and if players 3 and 4 won, you would send: '!score 1 2'",
        "After I get the score, I'll send you the next game. I'll keep track of how many games have been played.",
        "You can check the current scores/records at any point with !score. At the end of the mixup, I'll send you the final scores/records."
        "You can end the mixup at any point with !end. I'll send the scores then, as they are."
    ]
    for mess in messageArr:
        print(mess)
        await ctx.send(mess)

@bot.command()
async def setup4(ctx, p1, p2, p3, p4):
    playerArr.append(Player(str(p1)))
    playerArr.append(Player(str(p2)))
    playerArr.append(Player(str(p3)))
    playerArr.append(Player(str(p4)))

    random.shuffle(mixup.scheduleArr4)

    game = "GAME 1/9: " + playerArr[mixup.randSchedule4[0][0] - 1].name + ", " + playerArr[mixup.randSchedule[0][1] - 1].name + " vs. " + playerArr[mixup.randSchedule[0][2] - 1].name + ", " + playerArr[mixup.randSchedule[0][3] - 1].name
    await ctx.send("Setup Complete. " + game)

@bot.command()
async def result4(ctx, s1, s2):
    s1 = int(s1)
    s2 = int(s2)

    if (abs(s1-s2) > 4):
        await ctx.send("JESUS that's brutal...")

    #create a bool for if team 1 wins, figure out who each player is in the player array
    t1Win = (s1 > s2)
    p1 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][0] - 1]
    p2 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][1] - 1]
    p3 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][2] - 1]
    p4 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][3] - 1]

    num = random.randint(1,5)
    if num == 1:
        if t1Win:
            await ctx.send("Hey, chin up" + p3.name + " and " + p4.name + ". You'll do better next time I'm sure.")
        else:
            await ctx.send("Hey, chin up" + p1.name + " and " + p2.name + ". You'll do better next time I'm sure.")

    #update scores
    if t1Win:
        p1.wins += 1
        p2.wins += 1
        p3.losses += 1
        p4.losses += 1

        p1.goalsFor += s1
        p2.goalsFor += s1
        p3.goalsAgainst += s1
        p4.goalsAgainst += s1

        p1.goalsAgainst += s2
        p2.goalsAgainst += s2
        p3.goalsFor += s2
        p4.goalsFor += s2
    
    else:
        p1.losses += 1
        p2.losses += 1
        p3.wins += 1
        p4.wins += 1

        p1.goalsAgainst += s1
        p2.goalsAgainst += s1
        p3.goalsFor += s1
        p4.goalsFor += s1

        p1.goalsFor += s2
        p2.goalsFor += s2
        p3.goalsAgainst += s2
        p4.goalsAgainst += s2

    #increment num games played
    mixup.numGamesPlayed += 1

    #if there are more games to play
    if (mixup.numGamesPlayed < 9):
        #getting new players
        p1 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][0] - 1]
        p2 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][1] - 1]
        p3 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][2] - 1]
        p4 = playerArr[mixup.randSchedule4[mixup.numGamesPlayed][3] - 1]

        #send next game
        game = "GAME " + str(mixup.numGamesPlayed + 1) +"/9: " + p1.name + ", " + p2.name + " vs. " + p3.name + ", " + p4.name
        await ctx.send("Scores Updated.\n" + game)

    else:
        await ctx.send("Mixup finished, sending final scores.")
        recordArr = [[]]
        goalDiffArr = [[]]

        #Populate Ranking arrays
        for i in range(len(playerArr)):
            record = [(playerArr[i].wins - playerArr[i].losses), playerArr[i].name ]
            recordArr.append(record)
            
            goalDiff = [(playerArr[i].goalsFor - playerArr[i].goalsAgainst), playerArr[i].name]
            goalDiffArr.append(goalDiff)

        #Sort Ranking Arrays
        recordArr.sort(reverse=True)
        goalDiffArr.sort(reverse=True)

        for player in playerArr: 
            #assign players placement based on record
            for i in range(len(playerArr)):
                if (recordArr[i][1] == player.name):
                    player.placement = i + 1

            #output stats
            await ctx.send("\n==============================================\n")
            stats = str(player.name) + "\nWins: " + str(player.wins) + "\nLosses: " + str(player.losses) + "\nGoals For: " + str(player.goalsFor) + "\nGoals Against: " + str(player.goalsAgainst) + "\nOverall Placement: " + str(player.placement)
            await ctx.send(stats)

        #send overall placements
        await ctx.send("Overall Placements:")
        await ctx.send("\n==============================================\nGame Differentials:\n")
        for i in range(len(playerArr)):
            if recordArr[i][0] > 0:
                record = str(i + 1) + " " + str(recordArr[i][1]) + ": +" + str(recordArr[i][0])
            else:
                record = str(i + 1) + " " + str(recordArr[i][1]) + ":" + str(recordArr[i][0])
            await ctx.send(record)

        await ctx.send("\n==============================================\nGoal Differentials:\n")
        for i in range(len(playerArr)):
            if goalDiffArr[i][0] > 0:
                gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ": +" + str(goalDiffArr[i][0])
            else:
                gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ":" + str(goalDiffArr[i][0])
            await ctx.send(gd)

        await ctx.send("\n==============================================\nThanks for playing. Remember, you're all hot garbage at this game. Even you, " + str(recordArr[0][1]) + ".")

        #resetting for next mixup
        playerArr.clear()
        mixup.numGamesPlayed = 0

        
@bot.command()
async def setup(ctx, p1, p2, p3, p4, p5):

    #Populate player array
    playerArr.append(Player(str(p1)))
    playerArr.append(Player(str(p2)))
    playerArr.append(Player(str(p3)))
    playerArr.append(Player(str(p4)))
    playerArr.append(Player(str(p5)))

    #randomize schedule
    random.shuffle(mixup.randSchedule)

    #send first game in schedule
    game = "GAME 1/15: " + playerArr[mixup.randSchedule[0][0] - 1].name + ", " + playerArr[mixup.randSchedule[0][1] - 1].name + " vs. " + playerArr[mixup.randSchedule[0][2] - 1].name + ", " + playerArr[mixup.randSchedule[0][3] - 1].name
    await ctx.send("Setup Complete. " + game)

@bot.command()
async def result(ctx, s1, s2):

    s1 = int(s1)
    s2 = int(s2)

    if (abs(s1-s2) > 4):
        await ctx.send("JESUS that's brutal...")

    #create a bool for if team 1 wins, figure out who each player is in the player array
    t1Win = (s1 > s2)
    p1 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][0] - 1]
    p2 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][1] - 1]
    p3 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][2] - 1]
    p4 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][3] - 1]

    num = random.randint(1,5)
    if num == 1:
        if t1Win:
            await ctx.send("Hey, chin up" + p3.name + " and " + p4.name + ". You'll do better next time I'm sure.")
        else:
            await ctx.send("Hey, chin up" + p1.name + " and " + p2.name + ". You'll do better next time I'm sure.")

    #update scores
    if t1Win:
        p1.wins += 1
        p2.wins += 1
        p3.losses += 1
        p4.losses += 1

        p1.goalsFor += s1
        p2.goalsFor += s1
        p3.goalsAgainst += s1
        p4.goalsAgainst += s1

        p1.goalsAgainst += s2
        p2.goalsAgainst += s2
        p3.goalsFor += s2
        p4.goalsFor += s2
    
    else:
        p1.losses += 1
        p2.losses += 1
        p3.wins += 1
        p4.wins += 1

        p1.goalsAgainst += s1
        p2.goalsAgainst += s1
        p3.goalsFor += s1
        p4.goalsFor += s1

        p1.goalsFor += s2
        p2.goalsFor += s2
        p3.goalsAgainst += s2
        p4.goalsAgainst += s2

    #increment num games played
    mixup.numGamesPlayed += 1

    #if there are more games to play
    if (mixup.numGamesPlayed < 15):
        #getting new players
        p1 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][0] - 1]
        p2 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][1] - 1]
        p3 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][2] - 1]
        p4 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][3] - 1]

        #send next game
        game = "GAME " + str(mixup.numGamesPlayed + 1) +"/15: " + p1.name + ", " + p2.name + " vs. " + p3.name + ", " + p4.name
        await ctx.send("Scores Updated.\n" + game)

    else:
        await ctx.send("Mixup finished, sending final scores.")
        recordArr = [[]]
        goalDiffArr = [[]]

        #Populate Ranking arrays
        for i in range(len(playerArr)):
            record = [(playerArr[i].wins - playerArr[i].losses), playerArr[i].name ]
            recordArr.append(record)
            
            goalDiff = [(playerArr[i].goalsFor - playerArr[i].goalsAgainst), playerArr[i].name]
            goalDiffArr.append(goalDiff)

        #Sort Ranking Arrays
        recordArr.sort(reverse=True)
        goalDiffArr.sort(reverse=True)

        for player in playerArr: 
            #assign players placement based on record
            for i in range(len(playerArr)):
                if (recordArr[i][1] == player.name):
                    player.placement = i + 1

            #output stats
            await ctx.send("\n==============================================\n")
            stats = str(player.name) + "\nWins: " + str(player.wins) + "\nLosses: " + str(player.losses) + "\nGoals For: " + str(player.goalsFor) + "\nGoals Against: " + str(player.goalsAgainst) + "\nOverall Placement: " + str(player.placement)
            await ctx.send(stats)

        #send overall placements
        await ctx.send("Overall Placements:")
        await ctx.send("\n==============================================\nGame Differentials:\n")
        for i in range(len(playerArr)):
            if recordArr[i][0] > 0:
                record = str(i + 1) + " " + str(recordArr[i][1]) + ": +" + str(recordArr[i][0])
            else:
                record = str(i + 1) + " " + str(recordArr[i][1]) + ":" + str(recordArr[i][0])
            await ctx.send(record)

        await ctx.send("\n==============================================\nGoal Differentials:\n")
        for i in range(len(playerArr)):
            if goalDiffArr[i][0] > 0:
                gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ": +" + str(goalDiffArr[i][0])
            else:
                gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ":" + str(goalDiffArr[i][0])
            await ctx.send(gd)

        await ctx.send("\n==============================================\nThanks for playing. Remember, you're all hot garbage at this game. Even you, " + str(recordArr[0][1]) + ".")

        #resetting for next mixup
        playerArr.clear()
        mixup.numGamesPlayed = 0

@bot.command()
async def score(ctx):
    recordArr = [[]]
    goalDiffArr = [[]]

    #Populate Ranking arrays
    for i in range(len(playerArr)):
        record = [(playerArr[i].wins - playerArr[i].losses), playerArr[i].name ]
        recordArr.append(record)
        
        goalDiff = [(playerArr[i].goalsFor - playerArr[i].goalsAgainst), playerArr[i].name]
        goalDiffArr.append(goalDiff)

    #Sort Ranking Arrays
    recordArr.sort( reverse=True)
    goalDiffArr.sort( reverse=True)

    for player in playerArr: 
        #assign players placement based on record
        for i in range(len(playerArr)):
            if (recordArr[i][1] == player.name):
                player.placement = i + 1

        #output stats
        await ctx.send("\n==============================================\n")
        stats = str(player.name) + "\nWins: " + str(player.wins) + "\nLosses: " + str(player.losses) + "\nGoals For: " + str(player.goalsFor) + "\nGoals Against: " + str(player.goalsAgainst) + "\nOverall Placement: " + str(player.placement)
        await ctx.send(stats)

    #send overall placements
    await ctx.send("Overall Placements:")
    await ctx.send("\n==============================================\nGame Differentials:\n")
    for i in range(len(playerArr)):
        if recordArr[i][0] > 0:
            record = str(i + 1) + " " + str(recordArr[i][1]) + ": +" + str(recordArr[i][0])
        else:
            record = str(i + 1) + " " + str(recordArr[i][1]) + ":" + str(recordArr[i][0])
        await ctx.send(record)

    await ctx.send("\n==============================================\nGoal Differentials:\n")
    for i in range(len(playerArr)):
        if goalDiffArr[i][0] > 0:
            gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ": +" + str(goalDiffArr[i][0])
        else:
            gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ":" + str(goalDiffArr[i][0])
        await ctx.send(gd)

    await ctx.send("\n==============================================\n")

@bot.command()
async def end(ctx):
    await ctx.send("Ending the mixup here.")
    recordArr = [[]]
    goalDiffArr = [[]]

    #Populate Ranking arrays
    for i in range(len(playerArr)):
        record = [(playerArr[i].wins - playerArr[i].losses), playerArr[i].name ]
        recordArr.append(record)
        
        goalDiff = [(playerArr[i].goalsFor - playerArr[i].goalsAgainst), playerArr[i].name]
        goalDiffArr.append(goalDiff)

    #Sort Ranking Arrays
    recordArr.sort( reverse=True)
    goalDiffArr.sort( reverse=True)

    for player in playerArr: 
        #assign players placement based on record
        for i in range(len(playerArr)):
            if (recordArr[i][1] == player.name):
                player.placement = i + 1

        #output stats
        await ctx.send("\n==============================================\n")
        stats = str(player.name) + "\nWins: " + str(player.wins) + "\nLosses: " + str(player.losses) + "\nGoals For: " + str(player.goalsFor) + "\nGoals Against: " + str(player.goalsAgainst) + "\nOverall Placement: " + str(player.placement)
        await ctx.send(stats)

    #send overall placements
    await ctx.send("Overall Placements:")
    await ctx.send("\n==============================================\nGame Differentials:\n")
    for i in range(len(playerArr)):
        if recordArr[i][0] > 0:
            record = str(i + 1) + " " + str(recordArr[i][1]) + ": +" + str(recordArr[i][0])
        else:
            record = str(i + 1) + " " + str(recordArr[i][1]) + ":" + str(recordArr[i][0])

    await ctx.send("\n==============================================\nGoal Differentials:\n")
    for i in range(len(playerArr)):
        if goalDiffArr[i][0] > 0:
            gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ": +" + str(goalDiffArr[i][0])
        else:
            gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ":" + str(goalDiffArr[i][0])
        await ctx.send(gd)

    await ctx.send("\n==============================================\nThanks for playing. Remember, you're all hot garbage at this game. Even you, " + str(recordArr[0][1]) + ".")

    #resetting for next mixup
    playerArr.clear()
    mixup.numGamesPlayed = 0
    mixup.randSchedule = []

bot.run(TOKEN)