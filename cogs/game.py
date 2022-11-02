import discord
from discord.ext import commands
from parser import RockPaperScissorParser
from model import RPS
import random

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx, user_choice : RockPaperScissorParser):

        rpsm = RPS()
        bot_choice = random.choice(rpsm.get_choices)

        winner_check = {
            (RPS.ROCK, RPS.PAPER) : False,
            (RPS.ROCK, RPS.SCISSOR) : True,
            (RPS.PAPER, RPS.ROCK) : True,
            (RPS.PAPER, RPS.SCISSOR) : False,
            (RPS.SCISSOR, RPS.ROCK) : False,
            (RPS.SCISSOR, RPS.PAPER) : True,
        }
        won = None
        if bot_choice == user_choice:
            won = None
        else:
            won = winner_check[(user_choice, bot_choice)]
        
        if won is None:
            message = "It's a draw : %s vs %s"%(user_choice, bot_choice)
        elif won is True:
            message = "You won : %s vs %s"%(user_choice, bot_choice)
        elif won is False:
            message = "You lose : %s vs %s"%(user_choice, bot_choice)

        await ctx.send(user_choice.choice)
        