import os
from discord.ext import commands
from core.config import Config


class Bot(commands.Bot):
    def __init__(self, configpath: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configpath = configpath
        self.config = Config()

    def load_config(self):
        """ Loads config from JSON file """
        if os.path.isfile(self.configpath):
            with open(self.configpath, 'r') as f:
                self.config = Config.from_json(f.read())
        self.update_config()

    def update_config(self):
        """ Write current config state to JSON file """
        pretty = self.config.to_json(indent=2)
        with open(self.configpath, 'w') as f:
            f.write(pretty)
