import discord
class MixupEmbedder:

    embeds = []

    def embed_scores(self, mixup):
        recordArr = [[]]
        goalDiffArr = [[]]

        #Populate Ranking arrays
        for i in range(len(mixup.playerArr)):
            record = [(mixup.playerArr[i].wins - mixup.playerArr[i].losses), mixup.playerArr[i].name ]
            recordArr.append(record)
            
            goalDiff = [(mixup.playerArr[i].goalsFor - mixup.playerArr[i].goalsAgainst), mixup.playerArr[i].name]
            goalDiffArr.append(goalDiff)

        #Sort Ranking Arrays
        goalDiffArr.sort( reverse=True)
        recordArr.sort( reverse=True)
        message = ""

        tRecordArr = [[]]
        tGoalDiffArr = [[]]

        for i in range(len(mixup.teamArr)):
            record = [(mixup.teamArr[i].wins - mixup.teamArr[i].losses), mixup.teamArr[i].players ]
            tRecordArr.append(record)
        
            goalDiff = [(mixup.teamArr[i].goalsFor - mixup.teamArr[i].goalsAgainst), mixup.teamArr[i].players]
            tGoalDiffArr.append(goalDiff)

        
        tRecordArr.sort( reverse=True)
        tGoalDiffArr.sort( reverse=True)
        
        #output stats
        for team in mixup.teamArr:
            for i in range(len(mixup.teamArr)):
                if (tRecordArr[i][1] == team.players):
                    team.placement = i + 1
            embed = discord.Embed(title='Placement: '+str(team.placement), description="Team: "+str(team.players))
            embed.add_field(name='Record', value=str(team.wins)+'/'+str(team.losses), inline=False)
            embed.add_field(name="Goals For", value=str(team.goalsFor))
            embed.add_field(name="Goals Against", value=str(team.goalsAgainst))
            self.embeds.append(embed)

        for i in range(len(mixup.playerArr)):
            if tGoalDiffArr[i][0] > 0:
                gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ": +" + str(tGoalDiffArr[i][0])
            else:
                gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ":" + str(tGoalDiffArr[i][0])


        for player in mixup.playerArr: 
            #assign players placement based on record
            for i in range(len(mixup.playerArr)):
                if (recordArr[i][1] == player.name):
                    player.placement = i + 1

            #output stats
            embed = discord.Embed(title='Placement: '+str(player.placement), description="Name: "+str(player.name))
            embed.add_field(name='Record', value=str(player.wins)+"/"+str(player.losses), inline=False)
            embed.add_field(name="Goals For", value=str(player.goalsFor))
            embed.add_field(name="Goals Against", value=str(player.goalsAgainst))
            self.embeds.append(embed)

        return self.embeds