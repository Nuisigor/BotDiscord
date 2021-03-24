from discord import Forbidden
from discord import Intents
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, File
from ..db import db


#If You want to use this welcome cog, remember change the channel_id and the chat mentions


CHANNEL_ID = 822642985744334849



class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Welcome")


        embed = Embed(title="O bot está online!", description="Utilize o chat <#750083596882018367> para conversar com outros membros" ,color=0x11ff00)
        embed.add_field(name="Para obter ajuda sobre as funcionalidades do bot digite", value=f"> {self.bot.prefix}HelpAulas", inline=False)
        embed.set_thumbnail(url=self.bot.guild.icon_url)
        embed.set_footer(text=f"Discord da panelinha V{self.bot.VERSION}")
        channel = self.bot.get_channel(CHANNEL_ID)
        await channel.send(embed= embed)
    
    @Cog.listener()
    async def on_member_join(self, member): #Not Working Yet
        print("member joined")

    @Cog.listener()
    async def on_member_removed(self, member):  #Not Working yet
        print('member removed')
    
    


def setup(bot):
	bot.add_cog(Welcome(bot))