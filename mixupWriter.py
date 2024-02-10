class MixupWriter:

    def print_scores(self, mixup):
        recordArr = [[]]
        goalDiffArr = [[]]

        #Populate Ranking arrays
        for i in range(len(mixup.playerArr)):
            record = [(mixup.playerArr[i].wins - mixup.playerArr[i].losses), mixup.playerArr[i].name ]
            recordArr.append(record)
            
            goalDiff = [(mixup.playerArr[i].goalsFor - mixup.playerArr[i].goalsAgainst), mixup.playerArr[i].name]
            goalDiffArr.append(goalDiff)

        #Sort Ranking Arrays
        recordArr.sort( reverse=True)
        goalDiffArr.sort( reverse=True)
        message = ""

        if (mixup.type != 6):
            tRecordArr = [[]]
            tGoalDiffArr = [[]]

            for i in range(len(mixup.teamArr)):
                record = [(mixup.teamArr[i].wins - mixup.teamArr[i].losses), mixup.teamArr[i].players ]
                tRecordArr.append(record)
            
                goalDiff = [(mixup.teamArr[i].goalsFor - mixup.teamArr[i].goalsAgainst), mixup.teamArr[i].players]
                tGoalDiffArr.append(goalDiff)

            
            tRecordArr.sort( reverse=True)
            tGoalDiffArr.sort( reverse=True)

            message +=("TEAM STATS")
            
            #output stats
            for team in mixup.teamArr:
                for i in range(len(mixup.teamArr)):
                    if (tRecordArr[i][1] == team.players):
                        team.placement = i + 1

                message +=("\n#==============================================\n")
                stats = str(team.players) + "\nWins: " + str(team.wins) + "\nLosses: " + str(team.losses) + "\nGoals For: " + str(team.goalsFor) + "\nGoals Against: " + str(team.goalsAgainst) + "\nOverall Placement: " + str(team.placement)
                message +=("#"+stats)

            message +=("\nOverall Placements:")
            message +=("\n==============================================\nGame Differentials:\n")
            for i in range(len(mixup.playerArr)):
                if tRecordArr[i][0] > 0:
                    record = str(i + 1) + " " + str(tRecordArr[i][1]) + ": +" + str(tRecordArr[i][0])
                else:
                    record = str(i + 1) + " " + str(tRecordArr[i][1]) + ":" + str(tRecordArr[i][0])
                message +=("#"+record)

            message +=("\n==============================================\nGoal Differentials:\n")
            for i in range(len(mixup.playerArr)):
                if tGoalDiffArr[i][0] > 0:
                    gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ": +" + str(tGoalDiffArr[i][0])
                else:
                    gd = str(i + 1) + " " + str(tGoalDiffArr[i][1]) + ":" + str(tGoalDiffArr[i][0])
                message +=("#"+gd)

            message +=("\n==============================================\n")

        message +=("INDIVIDUAL STATS")
        for player in mixup.playerArr: 
            #assign players placement based on record
            for i in range(len(mixup.playerArr)):
                if (recordArr[i][1] == player.name):
                    player.placement = i + 1

            #output stats
            message +=("\n==============================================\n")
            stats = str(player.name) + "\nWins: " + str(player.wins) + "\nLosses: " + str(player.losses) + "\nGoals For: " + str(player.goalsFor) + "\nGoals Against: " + str(player.goalsAgainst) + "\nOverall Placement: " + str(player.placement)
            message +=("#"+stats)

        #send overall placements
        message +=("Overall Placements:")
        message +=("\n==============================================\nGame Differentials:\n")
        for i in range(len(mixup.playerArr)):
            if recordArr[i][0] > 0:
                record = str(i + 1) + " " + str(recordArr[i][1]) + ": +" + str(recordArr[i][0])
            else:
                record = str(i + 1) + " " + str(recordArr[i][1]) + ":" + str(recordArr[i][0])
            message +=("#"+record)

        message +=("\n==============================================\nGoal Differentials:\n")
        for i in range(len(mixup.playerArr)):
            if goalDiffArr[i][0] > 0:
                gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ": +" + str(goalDiffArr[i][0])
            else:
                gd = str(i + 1) + " " + str(goalDiffArr[i][1]) + ":" + str(goalDiffArr[i][0])
            message +=("#"+gd)

        message +=("\n==============================================")
        return message