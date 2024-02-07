#thiccBot.py

import itertools
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
    randSchedule = []
    team_size = 0

mixup = Mixup()
playerArr = []
teamArr = []

async def start_game(ctx, mixer: Mixup):
    nextGame = "GAME " + str(mixer.numGamesPlayed + 1) + "/" + str(mixup.maxGames) + ":" 
    
    for x in range(mixup.team_size * 2):
        nextGame += mixer.randSchedule[0][x]
    await ctx.send(nextGame)

def generate_schedule(players, teamsize):
    games = list(itertools.combinations(players, teamsize * 2))

    matchups = []
    for game in games:
        teams = list(itertools.combinations(game, teamsize))
        teams_len = len(teams)
        for x in range(0, int(teams_len/2)):
            matchups.append(teams[x] + teams.pop())
    random.shuffle(matchups)
    return matchups

def generate_teams(players, teamsize):
    return list(itertools.combinations(players, teamsize))

def initialize_mixup(players, teamsize):
    mixup.randSchedule = generate_schedule(players, teamsize)
    mixup.maxGames = len(mixup.randSchedule)
    mixup.team_size = teamsize
    teams = []
    teams = generate_teams(players, teamsize)
    for team in teams:
        teamArr.append(Team(team))
    for player in players:
        playerArr.append(Player(str(player)))
    print("Schedule:")
    print(mixup.randSchedule)

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
async def start(ctx, *args):
    if len(args) > 0:
        await ctx.send("Use the command by itself")
        return
    await ctx.send("Let's begin a mixup!", view=BeginButton())

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
        await start_game(ctx, mixup)

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
    game = mixup.randSchedule.pop(0)
    t1 = teamArr[0]
    t2 = teamArr[1]
    print(game[:mixup.team_size])
    print(game[mixup.team_size:])
    for team in teamArr:
        if (set(team.players) == set(game[:mixup.team_size])):
            t1 = team
        elif (set(team.players) == set(game[mixup.team_size:])):
            t2 = team
    for index, player in enumerate(playerArr):
        for x, baller in enumerate(game):
            if player.name == baller:
                if x < mixup.team_size / 2:
                    if t1Win:
                        player.wins+=1
                    else:
                        player.losses+=1
                    player.goalsFor+=s1
                    player.goalsAgainst+=s2
                else:
                    if not t1Win:
                        player.wins+=1
                    else:
                        player.losses+=1
                    player.goalsFor+=s2
                    player.goalsAgainst+=s1
    if t1Win:
        t1.wins += 1
        t2.losses += 1
    if not t1Win:
        t2.wins += 1
        t1.losses += 1

    t1.goalsFor += s1
    t2.goalsAgainst += s1
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

class BeginButton(discord.ui.View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Begin Mixup",style=discord.ButtonStyle.green)
    async def green_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        await interaction.response.send_modal(InformationModal())

class InformationModal(discord.ui.Modal, title='Setup Information Input'):

    player_names = discord.ui.TextInput(label='Player Names:', required=True, placeholder='Enter player names with spaces')
    team_size = discord.ui.TextInput(placeholder='Enter team size...', label='Team Size:', required=True)

    async def on_submit(self, interaction: discord.Interaction):
        individuals = self.player_names.value.split(' ')
        if len(individuals) < int(self.team_size.value)*2:
            await interaction.response.send_message("Oh no! There are less people than can make 2 teams!")
        else:
            await interaction.response.send_message("Thank you for submitting the mixup information. May the games begin!")
            initialize_mixup(individuals, int(self.team_size.value))
            await start_game(interaction.channel, mixup)
bot.run(TOKEN)