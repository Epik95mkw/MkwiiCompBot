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
    async def set_host_channel(self, interaction: discord.Interaction):
        """ Use this in the channel where submissions should be sent. """
        self.bot.config.submission_channel_id = interaction.channel.id
        self.bot.update_config()
        await respond(interaction, 'Submission channel set to this channel')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def set_submissions_message_channel(self, interaction: discord.Interaction):
        """ Use this in the channel where the current submissions message should be sent. """
        channel_id = self.bot.config.submissions_message.channel_id
        message_id = self.bot.config.submissions_message.message_id

        if channel_id == interaction.channel.id:
            await respond(interaction, 'Submission message channel is already set to this channel')
            return

        if channel_id is not None and message_id is not None:
            old_channel = interaction.guild.get_channel(channel_id)
            if old_channel is not None:
                old_message = await old_channel.fetch_message(message_id)
                if old_message is not None:
                    await old_message.delete()

        new_message = await interaction.channel.send(
            '__**Current Submissions:**__\n' +
            '\n'.join(f'{i + 1}. {username}' for i, username in enumerate(self.bot.config.task.submissions.keys()))
        )

        self.bot.config.submissions_message.channel_id = interaction.channel.id
        self.bot.config.submissions_message.message_id = new_message.id
        self.bot.update_config()
        await respond(interaction, 'Submission channel set to this channel')


    @slash_command(name='test')
    @guild_only()
    @default_permissions()
    async def say_hi(self, interaction: discord.Interaction):
        """ Test command """
        await respond(interaction, 'hi')
