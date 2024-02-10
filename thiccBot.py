#thiccBot.py

import os 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import mixup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD1')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def Message_Contains_Responses(message):
    msg = str(message.content).lower()
    if 'thiccbot' in msg or 'thiccbot' in str(message.mentions).lower():
        await message.channel.send("I'm back bitches.")

mixup = mixup.Mixup()

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

    await mixup.result(s1, s2, ctx)

@bot.command()
async def score(ctx):
    await mixup.sendScores(ctx)

@bot.command()
async def end(ctx):
    await mixup.end()

def updateScores(s1, s2):
    mixup.updateScores(s1, s2)

def message_split(message: str):
        return message.split('/n')


@bot.command()
async def writeScores(ctx):
    await mixup.writeScores()

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
            mixup.initialize_mixup(individuals, int(self.team_size.value))
            await mixup.start_game(interaction.channel)
bot.run(TOKEN)