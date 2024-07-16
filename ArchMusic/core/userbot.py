import sys
import asyncio
from datetime import timedelta
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        super().__init__(
            "ArchMusicString1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.restart_interval = timedelta(hours=1)
        
        self.two = Client(
            "ArchMusicString2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            "ArchMusicString3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            "ArchMusicString4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            "ArchMusicString5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistant Clients")
        
        clients = [self.one, self.two, self.three, self.four, self.five]
        
        for client in clients:
            if client == self.one and config.STRING1:
                await client.start()
            elif client == self.two and config.STRING2:
                await client.start()
            elif client == self.three and config.STRING3:
                await client.start()
            elif client == self.four and config.STRING4:
                await client.start()
            elif client == self.five and config.STRING5:
                await client.start()
            
            try:
                await client.join_chat("ARCH_SUPPORTS")
                await client.join_chat("ARCH_SUPPORTS")
                await client.join_chat("ARCH_SUPPORTS")
            except Exception as e:
                LOGGER(__name__).error(f"Assistant Account {clients.index(client)+1} failed to join chats: {e}")
            
            assistants.append(clients.index(client) + 1)
            
            try:
                await client.send_message(
                    config.LOG_GROUP_ID, "Asistan Başarıyla Başlatıldı 🥀"
                )
            except Exception as e:
                LOGGER(__name__).error(f"Assistant Account {clients.index(client)+1} failed to access the log Group: {e}")
                sys.exit()
            
            get_me = await client.get_me()
            client.username = get_me.username
            client.id = get_me.id
            assistantids.append(get_me.id)
            
            if get_me.last_name:
                client.name = get_me.first_name + " " + get_me.last_name
            else:
                client.name = get_me.first_name
            
            LOGGER(__name__).info(f"Assistant {clients.index(client)+1} Started as {client.name}")
        
        self.schedule_restart()

    async def restart_bot(self):
        LOGGER(__name__).info("Asistanlar yeniden başlatılıyor...")
        await self.stop()
        await self.start()

    def schedule_restart(self):
        loop = asyncio.get_event_loop()
        
        async def restart_at_intervals():
            while True:
                await asyncio.sleep(self.restart_interval.total_seconds())
                await self.restart_bot()

        loop.create_task(restart_at_intervals())
