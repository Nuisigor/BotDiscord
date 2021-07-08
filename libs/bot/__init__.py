from glob import glob
from asyncio import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
import discord
from ..db import db


#If you want to use this bot on your server remember change the guild id

PREFIX = "-"
OWNER_IDS = [241619682443001856]
GUILD_ID = 620693436408004619
# GUILD_ID = 750083596882018364
COGS = ["embeds", "aulas"]

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])



class Bot(BotBase):
    def __init__(self):
        self.prefix = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix = PREFIX, owner_ids = OWNER_IDS)


    def setup(self):
        for cog in COGS:
            self.load_extension(f"libs.cogs.{cog}")
            print(f"{cog} cog loaded")
        print("Setup complete")    


    def run(self, version):
        self.VERSION = version

        print("Running setup...")
        self.setup()

        with open("./libs/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    

    async def on_connected(self):
        print("Connected")
    
    async def on_disconnect(self):
        print("Disconnected")
    

    async def on_ready(self):
        if not self.ready:
            self.scheduler.start()
            self.guild = self.get_guild(GUILD_ID)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("Bot ready")
        
        else:
            print("Bot Reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)



bot = Bot()