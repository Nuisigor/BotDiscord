from discord import Forbidden
from discord import Intents
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, File
import discord

from ..db import db

#If You want to use this welcome cog, remember change the channel_id and the chat mentions

CHANNEL_ID = 740272013339394150 #TEST SERVER
# CHANNEL_ID = 822642985744334849

intents = Intents()
intents.default()
intents.members = True


class Embeds(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Embeds")

        
        Cog(intents= intents)

        embed = Embed(title="O bot está online!", description="Utilize o chat <#750083596882018367> para conversar com outros membros" ,color=0x11ff00)
        embed.add_field(name="Para obter ajuda sobre as funcionalidades do bot digite", value=f"> {self.bot.prefix}HelpAulas", inline=False)
        embed.set_thumbnail(url=self.bot.guild.icon_url)
        embed.set_footer(text=f"Discord da panelinha V{self.bot.VERSION}")
        channel = self.bot.get_channel(CHANNEL_ID)
        await channel.send(embed= embed)
        await self.bot.change_presence(activity=discord.Game(name=f"{self.bot.prefix}HelpAulas"), status=discord.Status.online)

    


    


def setup(bot):
    EmbedsCog = Embeds(bot)
    bot.add_cog(EmbedsCog)