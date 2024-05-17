import discord
from discord.ext import commands
from discord.app_commands import command as slash_command, default_permissions, guild_only

from core.bot import Bot


async def respond(interaction, msg):
    """ Helper function for responding with interactions """
    await interaction.response.send_message(msg, ephemeral=True)


class SlashCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    @guild_only()
    @default_permissions()
    async def setup(self, interaction: discord.Interaction, host_channel_id: int):
        """ Setup command. This should be run immediately after the bot is added to your server. """
        if self.bot.config.guild_id == interaction.guild.id:
            await respond(interaction, 'Server has already been configured.')
            return
        self.bot.config.guild_id = interaction.guild.id
        self.bot.config.submission_channel_id = host_channel_id
        self.bot.update_config()
        await respond(interaction, 'Bot configured for this server.')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def server_settings(
            self,
            interaction: discord.Interaction,
            host_channel_id: int = None,
            submission_list_channel_id: int = None
    ):
        """ Update one or more server settings directly. """
        if self.bot.config.guild_id != interaction.guild.id:
            await respond(interaction, 'Server has never been configured. Run /setup before using other commands.')
            return

        response_parts = []

        if host_channel_id is not None:
            self.bot.config.submission_channel_id = host_channel_id
            response_parts.append(f'Host channel updated to {host_channel_id}')

        if submission_list_channel_id is not None:
            self.bot.config.submissions_message.channel_id = submission_list_channel_id
            response_parts.append(f'Submission message channel updated to {submission_list_channel_id}')

        if response_parts:
            self.bot.update_config()
            await respond(interaction, '\n'.join(response_parts))
        else:
            await respond(interaction, 'No settings updated.')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def set_active_guild(self, interaction: discord.Interaction):
        """ Set bot's active guild to the current server. """
        self.bot.config.guild_id = interaction.guild.id
        self.bot.update_config()
        await respond(interaction, 'Active guild set to this server')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def set_submission_files_channel(self, interaction: discord.Interaction):
        """ Use this in channel where submissions should be sent. """
        self.bot.config.submission_channel_id = interaction.channel.id
        self.bot.update_config()
        await respond(interaction, 'Submission channel set to this channel')

    @slash_command()
    @guild_only()
    @default_permissions()
    async def set_submission_list_channel(self, interaction: discord.Interaction):
        """ Use this in channel where submissions should be sent. """
        self.bot.config.submission_channel_id = interaction.channel.id
        self.bot.update_config()
        await respond(interaction, 'Submission channel set to this channel')


    @slash_command(name='test')
    @guild_only()
    @default_permissions()
    async def say_hi(self, interaction: discord.Interaction):
        """ Test command """
        await respond(interaction, 'hi')
