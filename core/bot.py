import os
from typing import Optional

import discord
from discord.ext import commands
from core.config import Config


class Bot(commands.Bot):
    """
    Main bot class. This extends discord.py's Bot to store and modify config state.

    discord.Bot reference: https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?highlight=bot#bot
    """
    def __init__(self, configpath: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configpath = configpath
        self.config = Config()
        self._prev_config = None


    @property
    def active_guild(self) -> Optional[discord.Guild]:
        """ Get current active guild as a discord.Guild object. """
        return self.get_guild(self.config.guild_id or -1)


    def load_config(self):
        """ Load config from JSON file. """
        if os.path.isfile(self.configpath):
            with open(self.configpath, 'r') as f:
                self.config = Config.from_json(f.read())
        self.update_config()


    def update_config(self):
        """ Write current config state to JSON file and dispatch relevant events. """
        pretty = self.config.to_json(indent=2)
        with open(self.configpath, 'w') as f:
            f.write(pretty)
        if self._prev_config is not None:
            self._on_update(self._prev_config, self.config)
        self._prev_config = Config.from_json(self.config.to_json())


    def _on_update(self, old_config: Config, new_config: Config):
        """
        Internal function that gets called in ``update_config``. Compares the current
        config state to the previous one, and dispatches events based on which parts have changed.
        """
        if (old := old_config.host_channel_id) != (new := new_config.host_channel_id):
            self.dispatch('update_host_channel', old, new)

        if (old := old_config.submissions_message.channel_id) != (new := new_config.submissions_message.channel_id):
            self.dispatch('update_submission_message_channel', old, new)

        if (old := old_config.task.submissions) != (new := new_config.task.submissions):
            self.dispatch('update_submissions', old, new)
