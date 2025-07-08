# ==========================
# config.py content (place in config.py file)
# ==========================
API_HASH = "8f15d1722244d7e6d43570cff518cc5b"
APP_ID = 26459789
TG_BOT_TOKEN = "8062777752:AAE6K7xf8GxFpBbeT59XjRDPnzNyTdKkq9Y"
OWNER_ID = 7085291833
CHANNEL_ID = -1002604592369

TG_BOT_WORKERS = 10
ADMINS = [7085291833]
FORCE_SUB_CHANNEL = None
FORCE_SUB_CHANNEL2 = None
PORT = 8080
LOGGER = print

# ==========================
# jack-main_bot.py content
# ==========================

from aiohttp import web
from database.database import full_adminbase
from plugins import web_server
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from pyromod import listen
from datetime import datetime

from config import ADMINS, API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL,FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT, OWNER_ID


# fix for current pyrogram 
from pyrogram import utils

def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"
utils.get_peer_type = get_peer_type_new



class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        print(ADMINS)
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                sys.exit()
        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL2}")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            sys.exit()
        
        initadmin = await full_adminbase()
        for x in initadmin:
            if x in ADMINS:
                continue
            ADMINS.append(x)
        await self.send_message(
            chat_id=OWNER_ID,
            text="𝙼𝚊𝚜𝚝𝚎𝚛 𝚈𝚘𝚞𝚛 𝙱𝚘𝚝 𝙷𝚊𝚜 𝙱𝚎𝚎𝚗 𝚂𝚝𝚊𝚛𝚝𝚎𝚍!"
        )

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"𝚃𝚑𝚒𝚜 𝙱𝚘𝚝 𝙸𝚜 𝙼𝚊𝚍𝚎 𝙱𝚢 @Yae_X_Miko!")
        self.username = usr_bot_me.username


        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("𝚈𝚘𝚞𝚛 𝙱𝚘𝚝 𝙷𝚊𝚜 𝙱𝚎𝚎𝚗 𝚂𝚝𝚘𝚙𝚙𝚎𝚍 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 @Yae_X_Miko")

