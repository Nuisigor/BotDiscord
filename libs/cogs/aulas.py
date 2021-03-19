from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, File
from ..db import db

MEETLINK = "https://meet.google.com/"

class Aulas(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
    
    @command(name = "RegAula")
    async def register(self, ctx):
        message_content = ctx.message.content[9:]
        register_content = message_content.split(" ")

        if len(register_content[0]) > 3 or register_content[1][0:24] != MEETLINK:
            embed= Embed(title='Não foi possível registrar aula', description='Verifique as instruções de como utilizar o bot', color=0x0011ff)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name= 'Instruções',value='+RegAula Matéria Link', inline=True)
            embed.add_field(name = 'Exemplo',value='+RegAula POO https://meet.google.com/znc-asxa-uvw', inline=False)
            embed.set_footer(text='Cada matéria pode aceitar 3 caracteres apenas')
            await ctx.send(embed=embed)
        
        elif db.record("SELECT AulaID FROM Aulas WHERE AulaID = ?", register_content[0]) != None:
            embed= Embed(title="Aula já cadastrada :thumbsup:", description=f"Tente: +Aula {register_content[0]}", color=0x0011ff)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

        else:
            register_content.append(register_content[1] + "?pli=1&authuser=2")
            convert_register = [tuple(register_content)]
            print(convert_register)
            db.multiexec("INSERT INTO Aulas VALUES (?, ?, ?)", convert_register)
            db.commit()

            embed= Embed(title=f"Aula {register_content[0]} cadastrada", description=f"Para usar digite +Aula {register_content[0]}", color=0x0011ff)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f"Se Preferir utilize +Link {register_content[0]}")
            await ctx.send(embed=embed)


    @command(name = "DelAula")
    async def deleteAula(self, ctx):
        if ctx.author.id == self.bot.owner_ids[0]:
            message_content = ctx.message.content[9:]
            aula = db.execute('DELETE FROM Aulas WHERE AulaID = ?', message_content)
            db.commit()

            embed = Embed(title=f"Aula {message_content} deletada do banco :thumbsup:", color=0xff0000)
            await ctx.send(embed=embed)
    

    @command(name = "Aula", aliases=["Link"])
    async def sendLinks(self, ctx):
        message_content = ctx.message.content[6:]
        if len(message_content) > 3:
            pass
        else:
            aula = db.record('SELECT * FROM Aulas WHERE AulaID = ?', message_content)
            if aula != None:
                embed= Embed(title=f"Aula de {aula[0]}", color=0x00ff4c)
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.add_field(name='Link 1', value=aula[1], inline=True)
                embed.add_field(name='Link 2', value=aula[2], inline=False)
                await ctx.send(embed=embed)
    

    @command(name = "HelpAulas")
    async def sendHelp(self, ctx):
        embed= Embed(title="Precisando de Ajuda?", description="Comandos do bot de aula", color=0xeeff00)
        embed.add_field(name="Registrar Aula", value="+RegAula Matéria LinkDoMeets", inline=False)
        embed.add_field(name="Procurar Aulas", value="+Aula Matéria", inline=False)
        embed.set_footer(text="Futuramente pode ser adicionado mais funções")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Aulas(bot))