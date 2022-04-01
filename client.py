import dotenv, coloredlogs, logging

from yaml import load, dump, Loader, Dumper
from os import getenv as env
from pyrogram import Client, filters

dotenv.load_dotenv()
coloredlogs.install(level="WARNING")


class Client(Client):
    working_chat = -1001460724046
    katsu = 600432868
    filters = filters
    session_name = "service/asmr_autosend"
    db = session_name + ".yml"

    def __init__(self):
        super().__init__(
            session_name=self.session_name,
            api_id=env("API_ID"),
            api_hash=env("API_HASH"),
            bot_token=env("BOT_TOKEN"),
        )
        logging.warning("App initialized")

        db = self.load()
        if db is None:
            db = {
                "sent": [],
                "unsent": [],
            }
        self.dump(db)

    def load(self):
        with open(self.db, "r") as file:
            return load(file, Loader=Loader)

    def dump(self, yml):
        with open(self.db, "w") as file:
            return dump(yml, file, Dumper=Dumper)
