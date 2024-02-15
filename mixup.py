from datetime import datetime
import itertools
import os
import random
import discord
import mixupEmbedder
import mixupWriter


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
    playerArr = []
    teamArr = []


    async def start_game(self, ctx):
        nextGame = "GAME " + str(self.numGamesPlayed + 1) + "/" + str(self.maxGames) + ":" 
        
        for x in range(self.team_size * 2):
            nextGame += self.randSchedule[0][x] + ' '
            if (x==self.team_size - 1):
                nextGame+= 'vs. '
        await ctx.send(nextGame)

    def generate_schedule(self, players, teamsize):
        games = list(itertools.combinations(players, teamsize * 2))

        matchups = []
        for game in games:
            teams = list(itertools.combinations(game, teamsize))
            teams_len = len(teams)
            for x in range(0, int(teams_len/2)):
                matchups.append(teams[x] + teams.pop())
        random.shuffle(matchups)
        return matchups

    def generate_teams(self, players, teamsize):
        return list(itertools.combinations(players, teamsize))

    def initialize_mixup(self, players, teamsize):
        self.randSchedule = self.generate_schedule(players, teamsize)
        self.maxGames = len(self.randSchedule)
        self.team_size = teamsize
        teams = []
        teams = self.generate_teams(players, teamsize)
        for team in teams:
            self.teamArr.append(Team(team))
        for player in players:
            self.playerArr.append(Player(str(player)))
        print("Schedule:")
        print(self.randSchedule)

    async def result(self, s1, s2, ctx):
        s1 = int(s1)
        s2 = int(s2)

        #maybe add some more options to this
        if (abs(s1-s2) > 4):
            await ctx.send("JESUS that's brutal...")

        self.updateScores(s1, s2)

        #increment num games played
        self.numGamesPlayed += 1

        #if there are more games to play
        if (self.numGamesPlayed < self.maxGames):
            await self.start_game(ctx)

        else:
            await ctx.send("Mixup finished, sending final scores.")
            await self.sendScores(ctx)
            await self.writeScores()

            #resetting for next mixup, in case thiccbot hasn't been restarted since then
            #theres probably a better way to ensure this doesnt get messy but eh
            self.playerArr.clear()
            self.numGamesPlayed = 0

    async def end(self, ctx):
        await ctx.send("Ending the mixup here.")
        await self.sendScores(ctx)
        await self.writeScores()

        #resetting for next mixup
        self.playerArr.clear()
        self.numGamesPlayed = 0
        self.randSchedule = []

    def updateScores(self, s1, s2):
        t1Win = s1 > s2
        game = self.randSchedule.pop(0)
        t1 = self.teamArr[0]
        t2 = self.teamArr[1]
        print(game[:self.team_size])
        print(game[self.team_size:])
        for team in self.teamArr:
            if (set(team.players) == set(game[:self.team_size])):
                t1 = team
            elif (set(team.players) == set(game[self.team_size:])):
                t2 = team
        for index, player in enumerate(self.playerArr):
            for x, baller in enumerate(game):
                if player.name == baller:
                    if x < self.team_size / 2:
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

    async def sendScores(self, ctx):
        embedder = mixupEmbedder.MixupEmbedder()
        embeds = embedder.embed_scores(self)
        for result_embed in embeds:
            await ctx.send(embed=result_embed)

    def message_split(self, message: str):
        split = message.split('#')
        print(split)
        return split
    
    async def writeScores(self):
        #creating a new file in the results folder, named the current datetime
        thisFolder = os.path.dirname(os.path.abspath(__file__))
        fileName = "results\\" + str(datetime.now().month) + "-" + str(datetime.now().day) + " " + str(datetime.now().hour) + "oclockish.txt"
        filePath = os.path.join(thisFolder, fileName)
        newFile = open(filePath, "a")

        writer = mixupWriter.MixupWriter()
        message = writer.print_scores(self)
        for phrase in self.message_split(message):
            newFile.write(phrase)