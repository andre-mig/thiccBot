#thiccBot.py

import os 
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD1')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

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

class Team:
    players = []
    wins = 0
    losses = 0
    goalsFor = 0
    goalsAgainst = 0
    placement = 0
    def __init__(self,players):
        self.players = players

class Mixup:
    type = 0
    numGamesPlayed = 0
    maxGames = 0
    scheduleArr = []
    randSchedule = []

mixup = Mixup()
playerArr = []
teamArr = []

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord.')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    await Message_Contains_Responses(message)

@bot.command()
async def botHelp(ctx):
    #This needs to be updated
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
        await ctx.send(mess)


@bot.command()
async def setup(ctx, *args):

    #Getting list of players from arguments
    if (len(args) < 4 or len(args) > 6):
        await ctx.send("I can only do 4, 5, or 6 person mixups.")
        return
    else:
        mixup.type = len(args)

    #Populate player array
    for player in args:
        playerArr.append(Player(str(player)))

    #wanted to create a switch case but pythons dumb
    if (mixup.type == 4):

        #setup mixup info
        mixup.maxGames = 9
        mixup.scheduleArr = [[0,1,2,3], [0,1,2,3], [0,1,2,3],
                            [0,2,1,3], [0,2,1,3], [0,2,1,3],
                            [0,3,1,2], [0,3,1,2], [0,3,1,2]]
        
        teams = [[0,1], [0,2], [0,3], [1,2], [1,3], [2,3]]
        for team in teams:
            teamArr.append(Team(team))
        
        mixup.randSchedule = mixup.scheduleArr
        random.shuffle(mixup.randSchedule)

        firstGame = "GAME 1/9: " + playerArr[mixup.randSchedule[0][0]].name + ", " + playerArr[mixup.randSchedule[0][1]].name + " vs. " + playerArr[mixup.randSchedule[0][2]].name + ", " + playerArr[mixup.randSchedule[0][3]].name
    
    elif (mixup.type == 5):
        mixup.maxGames = 15
        mixup.scheduleArr = [[0,1,2,3], [0,1,3,4], [0,1,2,4],
                            [0,2,1,3], [0,2,1,4], [0,2,3,4],
                            [0,3,1,2], [0,3,1,4], [0,3,2,4],
                            [0,4,1,2], [0,4,1,3], [0,4,2,3],
                            [1,2,3,4], [1,3,2,4], [1,4,2,3]]
        
        teams = [[0,1], [0,2], [0,3], [0,4],
                        [1,2], [1,3], [1,4], [2,3],
                        [2,4], [3,4]]
        
        for team in teams:
            teamArr.append(Team(team))

        mixup.randSchedule = mixup.scheduleArr
        random.shuffle(mixup.randSchedule)

        firstGame = "GAME 1/15: " + playerArr[mixup.randSchedule[0][0]].name + ", " + playerArr[mixup.randSchedule[0][1]].name + " vs. " + playerArr[mixup.randSchedule[0][2]].name + ", " + playerArr[mixup.randSchedule[0][3]].name
    
    elif (mixup.type == 6):
        mixup.maxGames = 10
        mixup.scheduleArr = [[0,1,2, 3,4,5], [0,1,3, 2,4,5], [0,1,4, 2,3,5], [0,1,5, 2,3,4],
                            [0,2,3, 1,4,5], [0,2,4, 1,3,5], [0,2,5, 1,3,4],
                            [0,3,4, 1,2,5], [0,3,5, 1,2,4], [1,2,3, 0,4,5], ]
        
        mixup.randSchedule = mixup.scheduleArr
        random.shuffle(mixup.randSchedule)

        firstGame = "GAME 1/10: " + playerArr[mixup.randSchedule[0][0]].name + ", " + playerArr[mixup.randSchedule[0][1]].name + ", " + playerArr[mixup.randSchedule[0][2]].name + " vs. " + playerArr[mixup.randSchedule[0][3]].name + ", " + playerArr[mixup.randSchedule[0][4]].name + ", " + playerArr[mixup.randSchedule[0][5]].name
    else:
        await ctx.send("mixup type incorrectly assigned")
        return

    #send first game in schedule
    await ctx.send("Setup Complete.\n" + firstGame)

@bot.command()
async def result(ctx, s1, s2):

    s1 = int(s1)
    s2 = int(s2)

    #maybe add some more options to this
    if (abs(s1-s2) > 4):
        await ctx.send("JESUS that's brutal...")

    updateScores(s1, s2)

    #increment num games played
    mixup.numGamesPlayed += 1

    #if there are more games to play
    if (mixup.numGamesPlayed < mixup.maxGames):
        #getting new players
        p1 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][0]]
        p2 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][1]]
        p3 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][2]]
        p4 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][3]]

        if (mixup.type == 6):
            p5 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][4]]
            p6 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][5]]

            nextGame = "GAME " + str(mixup.numGamesPlayed + 1) + "/" + str(mixup.maxGames) + ": " + p1.name + ", " + p2.name + ", " + p3.name + "vs. " + p4.name + "," + p5.name + ", " + p6.name
        
        else:
            nextGame = "GAME " + str(mixup.numGamesPlayed + 1) + "/" + str(mixup.maxGames) + ": " + p1.name + ", " + p2.name + " vs. " + p3.name + ", " + p4.name

        await ctx.send("Scores Updated.\n" + nextGame)

    else:
        await ctx.send("Mixup finished, sending final scores.")
        await sendScores(ctx)
        await writeScores()

        #resetting for next mixup, in case thiccbot hasn't been restarted since then
        #theres probably a better way to ensure this doesnt get messy but eh
        playerArr.clear()
        mixup.numGamesPlayed = 0

@bot.command()
async def score(ctx):
    await sendScores(ctx)

@bot.command()
async def end(ctx):
    await ctx.send("Ending the mixup here.")
    await sendScores(ctx)
    await writeScores()

    #resetting for next mixup
    playerArr.clear()
    mixup.numGamesPlayed = 0
    mixup.randSchedule = []

def updateScores(s1, s2):
    t1Win = s1 > s2
    if (mixup.type == 6):
        #Figure out who is who
        p1 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][0]]
        p2 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][1]]
        p3 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][2]]
        p4 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][3]]
        p5 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][4]]
        p6 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][5]]

        #update wins
        if t1Win:
            p1.wins += 1
            p2.wins += 1
            p3.wins += 1
            p4.losses += 1
            p5.losses += 1
            p6.losses += 1
        
        else:
            p1.losses += 1
            p2.losses += 1
            p3.losses += 1
            p4.wins += 1
            p5.wins += 1
            p6.wins += 1

        #update goals
        p1.goalsFor += s1
        p2.goalsFor += s1
        p3.goalsFor += s1
        p4.goalsAgainst += s1
        p5.goalsAgainst += s1
        p6.goalsAgainst += s1

        p1.goalsAgainst += s2
        p2.goalsAgainst += s2
        p3.goalsAgainst += s2
        p4.goalsFor += s2
        p5.goalsFor += s2
        p6.goalsFor += s2

    else:
        #Figure out which teams are playing
        for team in teamArr:
            if (team.players == [mixup.randSchedule[mixup.numGamesPlayed][0], mixup.randSchedule[mixup.numGamesPlayed][1]]):
                t1 = team
            elif (team.players == [mixup.randSchedule[mixup.numGamesPlayed][2], mixup.randSchedule[mixup.numGamesPlayed][3]]):
                t2 = team
        
        #figure out who is who
        p1 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][0]]
        p2 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][1]]
        p3 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][2]]
        p4 = playerArr[mixup.randSchedule[mixup.numGamesPlayed][3]]

        #update wins
        if t1Win:
            p1.wins += 1
            p2.wins += 1
            p3.losses += 1
            p4.losses += 1
            t1.wins += 1
            t2.losses += 1

        else: 
            p1.losses += 1
            p2.losses += 1
            p3.wins += 1
            p4.wins += 1
            t1.losses += 1
            t2.wins += 1

        #update goals
        p1.goalsFor += s1
        p2.goalsFor += s1
        p3.goalsAgainst += s1
        p4.goalsAgainst += s1
        t1.goalsFor += s1
        t2.goalsAgainst += s1

        p1.goalsAgainst += s2
        p2.goalsAgainst += s2
        p3.goalsFor += s2
        p4.goalsFor += s2
        t1.goalsAgainst += s2
        t2.goalsFor += s2
        

async def sendScores(ctx):
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

    if (mixup.type != 6):
        tRecordArr = [[]]
        tGoalDiffArr = [[]]

        for i in range(len(teamArr)):
            record = [(teamArr[i].wins - teamArr[i].losses), teamArr[i].players ]
            tRecordArr.append(record)
        
            goalDiff = [(teamArr[i].goalsFor - teamArr[i].goalsAgainst), teamArr[i].players]
            tGoalDiffArr.append(goalDiff)

        
        tRecordArr.sort( reverse=True)
        tGoalDiffArr.sort( reverse=True)

        await ctx.send("TEAM STATS")
        
        #output stats
        for team in teamArr:
            for i in range(len(teamArr)):
                if (tRecordArr[i][1] == team.players):
                    team.placement = i + 1

            await ctx.send("\n==============================================\n")
            stats = str(team.players) + "\nWins: " + str(team.wins) + "\nLosses: " + str(team.losses) + "\nGoals For: " + str(team.goalsFor) + "\nGoals Against: " + str(team.goalsAgainst) + "\nOverall Placement: " + str(team.placement)
            await ctx.send(stats)

        await ctx.send("Overall Placements:")
        await ctx.send("\n==============================================\nGame Differentials:\n")
        for i in range(len(playerArr)):
            if tRecordArr[i][0] > 0:
                record = str(i + 1) + " " + str(tRecordArr[i][1]) + ": +" + str(tRecordArr[i][0])
            else:
                record = str(i + 1) + " " + str(tRecordArr[i][1]) + ":" + str(tRecordArr[i][0])
            await ctx.send(record)

        await ctx.send("\n==============================================\nGoal Differentials:\n")
        for i in range(len(playerArr)):
            if tGoalDiffArr[i][0] > 0:
                gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ": +" + str(tGoalDiffArr[i][0])
            else:
                gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ":" + str(tGoalDiffArr[i][0])
            await ctx.send(gd)

        await ctx.send("\n==============================================\n")

    await ctx.send("INDIVIDUAL STATS")
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
async def writeScores(ctx):
    await writeScores()

async def writeScores():
    #creating a new file in the results folder, named the current datetime
    thisFolder = os.path.dirname(os.path.abspath(__file__))
    fileName = "results\\" + str(datetime.now().month) + "-" + str(datetime.now().day) + " " + str(datetime.now().hour) + "oclockish.txt"
    filePath = os.path.join(thisFolder, fileName)
    newFile = open(filePath, "a")

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

    if (mixup.type != 6):
        tRecordArr = [[]]
        tGoalDiffArr = [[]]

        for i in range(len(teamArr)):
            record = [(teamArr[i].wins - teamArr[i].losses), teamArr[i].players ]
            tRecordArr.append(record)
        
            goalDiff = [(teamArr[i].goalsFor - teamArr[i].goalsAgainst), teamArr[i].players]
            tGoalDiffArr.append(goalDiff)

        
        tRecordArr.sort( reverse=True)
        tGoalDiffArr.sort( reverse=True)

        newFile.write("TEAM STATS")
        
        #output stats
        for team in teamArr:
            for i in range(len(teamArr)):
                if (tRecordArr[i][1] == team.players):
                    team.placement = i + 1

            newFile.write("\n==============================================\n")
            stats = str(team.players) + "\nWins: " + str(team.wins) + "\nLosses: " + str(team.losses) + "\nGoals For: " + str(team.goalsFor) + "\nGoals Against: " + str(team.goalsAgainst) + "\nOverall Placement: " + str(team.placement)
            newFile.write(stats)

        newFile.write("Overall Placements:")
        newFile.write("\n==============================================\nGame Differentials:\n")
        for i in range(len(playerArr)):
            if tRecordArr[i][0] > 0:
                record = str(i + 1) + " " + str(tRecordArr[i][1]) + ": +" + str(tRecordArr[i][0])
            else:
                record = str(i + 1) + " " + str(tRecordArr[i][1]) + ":" + str(tRecordArr[i][0])
            newFile.write(record)

        newFile.write("\n==============================================\nGoal Differentials:\n")
        for i in range(len(playerArr)):
            if tGoalDiffArr[i][0] > 0:
                gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ": +" + str(tGoalDiffArr[i][0])
            else:
                gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ":" + str(tGoalDiffArr[i][0])
            newFile.write(gd)

        newFile.write("\n==============================================\n")

    newFile.write("INDIVIDUAL STATS")
    for player in playerArr: 
        #assign players placement based on record
        for i in range(len(playerArr)):
            if (recordArr[i][1] == player.name):
                player.placement = i + 1

        #output stats
        newFile.write("\n==============================================\n")
        stats = str(player.name) + "\nWins: " + str(player.wins) + "\nLosses: " + str(player.losses) + "\nGoals For: " + str(player.goalsFor) + "\nGoals Against: " + str(player.goalsAgainst) + "\nOverall Placement: " + str(player.placement)
        newFile.write(stats)

    #send overall placements
    newFile.write("Overall Placements:")
    newFile.write("\n==============================================\nGame Differentials:\n")
    for i in range(len(playerArr)):
        if recordArr[i][0] > 0:
            record = str(i + 1) + " " + str(recordArr[i][1]) + ": +" + str(recordArr[i][0])
        else:
            record = str(i + 1) + " " + str(recordArr[i][1]) + ":" + str(recordArr[i][0])
        newFile.write(record)

    newFile.write("\n==============================================\nGoal Differentials:\n")
    for i in range(len(playerArr)):
        if goalDiffArr[i][0] > 0:
            gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ": +" + str(goalDiffArr[i][0])
        else:
            gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ":" + str(goalDiffArr[i][0])
        newFile.write(gd)

    newFile.write("\n==============================================\n")
    
    newFile.close()
bot.run(TOKEN)