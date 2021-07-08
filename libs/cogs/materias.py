import discord
from discord.ext.commands import Cog
from ..db import db


class Materias(Cog):

    def __init__(self,bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Materias(bot))