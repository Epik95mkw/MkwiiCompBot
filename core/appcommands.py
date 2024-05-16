import discord
from discord.ext import commands
from discord.app_commands import command as slash_command, default_permissions, guild_only

from core.bot import Bot


async def respond(interaction, msg):
    """ Helper function for responding with interactions """
    await interaction.response.send_message(msg, ephemeral=True)


class AppCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name='test')
    @guild_only()
    @default_permissions()
    async def say_hi(self, interaction: discord.Interaction):
        """ Test command """
        await respond(interaction, 'hi')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def set_submission_channel(self, interaction: discord.Interaction):
        """ Use this in channel where submissions should be sent. """
        self.bot.config.submission_file_channel = interaction.channel.id
        self.bot.update_config()
        await respond(interaction, 'Submission channel set to this channel')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def get_all_submissions(self, interaction: discord.Interaction):
        """ Send zip of all current task submissions. """
        # https://www.neilgrogan.com/py-bin-zip/
        pass
