import asyncio
from datetime import datetime
import functools
import typing
import pygsheets
import pandas as pd
import mixup


class spreadsheetWriter:
    gc = pygsheets.authorize(service_file='credentials.json')
    workbook = gc.open('Mixup Results')
    recordArr = [[]]
    goalDiffArr = [[]]
    tRecordArr = [[]]
    tGoalDiffArr = [[]]

    def to_thread(func: typing.Callable) -> typing.Coroutine:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await asyncio.to_thread(func, *args, **kwargs)
        return wrapper


    @to_thread
    def write_results(self, mixup):

        #Populate Ranking arrays
        for i in range(len(mixup.playerArr)):
            record = [(mixup.playerArr[i].wins - mixup.playerArr[i].losses), mixup.playerArr[i].name ]
            self.recordArr.append(record)
            
            goalDiff = [(mixup.playerArr[i].goalsFor - mixup.playerArr[i].goalsAgainst), mixup.playerArr[i].name]
            self.goalDiffArr.append(goalDiff)

        #Sort Ranking Arrays
        self.goalDiffArr.sort( reverse=True)
        self.recordArr.sort( reverse=True)

        self.write_teams(mixup)
        self.write_players(mixup)


    def write_teams(self, mixup):
        sheet = self.workbook.add_worksheet(title="Teams " + str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year) + ' ' + str(datetime.now().hour)+ ':' + str(datetime.now().minute)+ ' ' + str(datetime.now().second))
        sheet.unlink()
        sheet.add_rows(1)
        headers = ['Placement', 'Team', 'Wins', 'Losses', 'Goals For', 'Goals Against']
        for x, header in enumerate(headers):
            sheet.update_value((1, x+1), header)

        for i in range(len(mixup.teamArr)):
            record = [(mixup.teamArr[i].wins - mixup.teamArr[i].losses), mixup.teamArr[i].players ]
            self.tRecordArr.append(record)
        
            goalDiff = [(mixup.teamArr[i].goalsFor - mixup.teamArr[i].goalsAgainst), mixup.teamArr[i].players]
            self.tGoalDiffArr.append(goalDiff)

        
        self.tRecordArr.sort( reverse=True)
        self.tGoalDiffArr.sort( reverse=True)
        
        #output stats
        for x, team in enumerate(mixup.teamArr):
            for i in range(len(mixup.teamArr)):
                if (self.tRecordArr[i][1] == team.players):
                    team.placement = i + 1
            sheet.update_value((x+2, 1), team.placement)
            sheet.update_value((x+2, 2), str(team.players))
            sheet.update_value((x+2, 3), team.wins)
            sheet.update_value((x+2, 4), team.losses)
            sheet.update_value((x+2, 5), team.goalsFor)
            sheet.update_value((x+2, 6), team.goalsAgainst)
        sheet.link()

    def write_players(self, mixup):
        sheet = self.workbook.add_worksheet(title="Individuals " + str(datetime.now().month) + "/" + str(datetime.now().day) + "/" + str(datetime.now().year) + ' ' + str(datetime.now().hour)+ ':' + str(datetime.now().minute)+ ' ' + str(datetime.now().second))
        sheet.unlink()
        sheet.add_rows(1)
        headers = ['Placement', 'Name', 'Wins', 'Losses', 'Goals For', 'Goals Against']
        for x, header in enumerate(headers):
            sheet.update_value((1, x+1), header)
        for x, player in enumerate(mixup.playerArr): 
            #assign players placement based on record
            for i in range(len(mixup.playerArr)):
                if (self.recordArr[i][1] == player.name):
                    player.placement = i + 1

            #output stats
            sheet.update_value((x+2, 1), player.placement)
            sheet.update_value((x+2, 2), player.name)
            sheet.update_value((x+2, 3), player.wins)
            sheet.update_value((x+2, 4), player.losses)
            sheet.update_value((x+2, 5), player.goalsFor)
            sheet.update_value((x+2, 6), player.goalsAgainst)
        sheet.link()
