import os

import discord
from discord.ext import commands
from core.config import Config


class Bot(commands.Bot):
    def __init__(self, configpath: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configpath = configpath
        self.config = Config()
        self._prev_config = None


    @property
    def active_guild(self) -> discord.Guild:
        return self.get_guild(self.config.guild_id or -1)


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
        if self._prev_config is not None:
            self._on_update(self._prev_config, self.config)
        self._prev_config = Config.from_json(self.config.to_json())


    def _on_update(self, old_config: Config, new_config: Config):
        if (old := old_config.host_channel_id) != (new := new_config.host_channel_id):
            self.dispatch('update_host_channel', old, new)

        if (old := old_config.submissions_message.channel_id) != (new := new_config.submissions_message.channel_id):
            self.dispatch('update_submission_message_channel', old, new)

        if (old := old_config.task.submissions) != (new := new_config.task.submissions):
            self.dispatch('update_submissions', old, new)


    # def submission_message(self):
    #     return (
    #         '__**Current Submissions:**__\n' +
    #         '\n'.join(f'{i + 1}. {username}' for i, username in enumerate(self.config.task.submissions.keys()))
    #     )
