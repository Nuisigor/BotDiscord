from libs.cogs.embeds import Embeds
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, File, message
from . import embeds

from ..db import db

DayofWeek = ['segunda','terça','quarta','quinta','sexta', 'seg', 'ter', 'qua', 'qui', 'sex', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']


MEETLINK = "https://meet.google.com/"

class Aulas(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Aulas")

    @command(name = "RegAula", aliases=['regaula'])
    async def register(self, ctx):
        message_content = ctx.message.content[9:]
        register_content = message_content.split(" ")

        register_content[0] = register_content[0].upper()
        print(register_content)


        if len(register_content[0]) > 15 or register_content[1][0:24] != MEETLINK:
            embed= Embed(title='Não foi possível registrar aula', description='Verifique as instruções de como utilizar o bot', color=0x0011ff)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name= 'Instruções',value=f'{self.bot.prefix}RegAula Matéria Link', inline=True)
            embed.add_field(name = 'Exemplo',value=f'{self.bot.prefix}RegAula POO https://meet.google.com/znc-asxa-uvw', inline=False)
            embed.set_footer(text='Cada matéria pode aceitar 15 caracteres apenas (Não abuse)')
            await ctx.send(embed=embed)

        elif db.record("SELECT AulaID FROM Aulas WHERE AulaID = ?", register_content[0]) != None:
            embed= Embed(title="Aula já cadastrada :thumbsup:", description=f"Tente: {self.bot.prefix}Aula {register_content[0]}", color=0x0011ff)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

        else:
            register_content.append(register_content[1] + "?pli=1&authuser=2")
            convert_register = [tuple(register_content)]
            print(convert_register)
            db.multiexec("INSERT INTO Aulas VALUES (?, ?, ?)", convert_register)
            db.commit()

            embed= Embed(title=f"Aula {register_content[0]} cadastrada", description=f"Para usar digite {self.bot.prefix}Aula {register_content[0]}", color=0x0011ff)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(text=f"Se Preferir utilize {self.bot.prefix}Link {register_content[0]}")
            await ctx.send(embed=embed)


    @command(name = "DelAula", aliases=['delaula'])
    async def deleteAula(self, ctx):
        if ctx.author.id == self.bot.owner_ids[0]:
            message_content = ctx.message.content[9:]

            message_content = message_content.upper()

            db.execute('DELETE FROM Aulas WHERE AulaID = ?', message_content)
            db.commit()

            embed = Embed(title=f"Aula {message_content} deletada do banco :thumbsup:", color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)


    @command(name = "Aula", aliases=['Link','aula','link'])
    async def sendLinks(self, ctx):
        message_content = ctx.message.content[6:]

        message_content = message_content.upper()

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


    @command(name = "ListarAulas", aliases=['listaraulas','Listaraulas','listarAulas'])
    async def listAulas(self, ctx):
        embed= Embed(title="Lista de Aulas cadastradas", color=0xc800ff)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        for aulaid in db.records('SELECT AulaID FROM Aulas'):
            embed.add_field(name=f"{aulaid[0]}", value=f"Comando: {self.bot.prefix}Aula {aulaid[0]}", inline=False)

        await ctx.send(embed= embed)

    @command(name = "HelpAulas", aliases=["helpaulas"])
    async def sendHelp(self, ctx):
        embed= Embed(title="Precisando de Ajuda?", description="Comandos do bot de aula", color=0xeeff00)
        embed.add_field(name="Registrar Aula", value=f"{self.bot.prefix}RegAula Matéria LinkDoMeets", inline=False)
        embed.add_field(name="Procurar Aulas", value=f"{self.bot.prefix}Aula Matéria", inline=False)
        embed.add_field(name="Listar Aulas", value=f"{self.bot.prefix}ListarAulas", inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text="Futuramente pode ser adicionado mais funções")
        await ctx.send(embed=embed)

    async def sendErrorRegisterScheduler(self,ctx):
        embed= Embed(title=":warning:Erro na criação da agenda", description="Algum erro aconteceu, veja se você utilizou o comando corretamente ou se a aula já contém um horário.", color=0xf00000)
        embed.add_field(name="Exemplo", value=f"> {self.bot.prefix}HorarioAula POO Segunda 19:30", inline=True)
        embed.add_field(name= "Verificando se a aula já possui horario registrado ", value=f"> {self.bot.prefix}Aula \"NOMEDAAULA\"", inline=True)
        # embed.set_thumbnail(url=self.bot.guild.icon_url)
        await ctx.send(embed=embed)

    @command(name = "HorarioAula", aliases=["horarioaula","horarioAula","HORARIOAULA","Horarioaula"])
    async def registerScheduler(self,ctx):
        message_content = ctx.message.content[13:]
        register_content = message_content.split(" ")
        if(len(register_content) == 3):
            register_content[0] = register_content[0].upper()


            register_content[1] = register_content[1].lower()

            if db.record("SELECT AulaID FROM Aulas WHERE AulaID = ?", register_content[0]) != None:
                flag = 0
                for i in range(len(DayofWeek)):            
                    if register_content[1] == DayofWeek[i]:
                        dayindex = i%5
                        register_content[1] = DayofWeek[dayindex]
                        if db.record("SELECT Aula FROM HorarioAulas WHERE Aula = ? AND DiaSemana = ?", register_content[0],register_content[1]) == None:

                            register_content[2] = register_content[2].split(":")
                            register_content[2][0] = int(register_content[2][0])
                            register_content[2][1] = int(register_content[2][1])

                            if register_content[2][0] >= 0 and register_content[2][0] <24:
                                if register_content[2][1] >=0 and register_content[2][1] < 60:
                                    flag = 1
                                    db_register = [register_content[0], register_content[1], dayindex, register_content[2][0], register_content[2][1]]
                                    db_register = [tuple(db_register)]
                                    db.multiexec("INSERT INTO HorarioAulas VALUES (?,?,?,?,?)", db_register)
                                    db.commit()
                                    print(db_register)
                                await ctx.send(f"Horario da Aula {register_content[0]} registrada")



                if flag == 0:
                    await self.sendErrorRegisterScheduler(ctx)
            else:
                await self.sendErrorRegisterScheduler(ctx)
        else:
            await self.sendErrorRegisterScheduler(ctx)
            # if db.record("SELECT AulaID FROM Aulas WHERE ID = ?", register_content[0]) != None:
            #     db.execute(f"INSERT INTO Aulas (DiaSemana, Hora, Minuto) VALUES ({register_content[1]}, {register_content[2][0]}, {register_content[2][1]})")

    @command(name = "DelHorarioAula", aliases=["delhorarioaula","DELHORARIOAULA"])
    async def deleteScheduler(self,ctx):
        delete_content = ctx.message.content[16:]
        delete_content = delete_content.split(" ")

        delete_content[0] = delete_content[0].upper()

        for i in range(len(DayofWeek)):            
                    if delete_content[1] == DayofWeek[i]:
                        dayindex = i%5
                        delete_content[1] = DayofWeek[dayindex]
        
        print(delete_content)

        if ctx.author.id == self.bot.owner_ids[0]:
            delete_content = [tuple(delete_content)]
            db.multiexec(f"DELETE FROM HorarioAulas WHERE Aula = ? AND DiaSemana = ?",delete_content)
            db.commit()
            delete_content = list(delete_content[0])
            embed = Embed(title=f"Horario de {delete_content[0]} da aula {delete_content[1]} deletada do banco :thumbsup:", color=0xff0000)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)

    @command(name = "VerHorario", aliases = ['verhorario','verhorarioaula','VerHorarioAula','VERHORARIOAULA','VERHORARIO'])
    async def SchedulerPreview(self,ctx):
        message_content = ctx.message.content
        message_content = message_content.split(" ")
        
        if len(message_content) == 1:
            aulas = db.records("SELECT DISTINCT Aula FROM HorarioAulas ORDER BY Aula")
            embed = Embed(title="Aulas com Horario")
            embed.set_thumbnail(url=ctx.guild.icon_url)
            for aula in aulas:
                    embed.add_field(name=f"Aula de {aula[0]}",value=f"{self.bot.prefix}VerHorario {aula[0]}", inline=False)
            await ctx.send(embed=embed)

        else:
            message_content[1] = message_content[1].upper()
            schedule = db.records("SELECT DiaSemana, Hora, Minuto FROM HorarioAulas WHERE Aula = ? ORDER BY DiaSemanaIndex",message_content[1])

            if schedule != []:
                embed = Embed(title=f"Horarios da aula de {message_content[1]}")
                for timetable in schedule:
                    embed.add_field(name=f"{timetable[0].capitalize()}-feira",value=f"{timetable[1]}:{timetable[2]}",inline=False)
                await ctx.send(embed=embed)
            
            else:
                embed = Embed(title="Erro na procura da aula", description="Algum erro aconteceu, veja se a aula já possui horarios", color=0xf00000)
                embed.add_field(name="Listando aulas cadastradas:",value="> -ListarAulas \"NomeDaAula\"")
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Aulas(bot))