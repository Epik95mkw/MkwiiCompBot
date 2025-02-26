import discord
from discord.ext import commands
from discord.app_commands import command as slash_command, default_permissions, guild_only

from core.bot import Bot
from core.config import Task


async def respond(interaction, msg):
    """ Helper function for responding with interactions """
    await interaction.response.send_message(msg, ephemeral=True)


class SlashCommands(commands.Cog):
    """
    Cog containing all slash commands. Access to these commands can be managed by server admins in Discord directly.
    Note that most commands should only update the relevant values in ``bot.config``; any logic depending on said values
    should be moved to a listener and called by dispatching a custom event in ``bot.update_config()``.

    Slash command reference:
    https://discordpy.readthedocs.io/en/stable/interactions/api.html?highlight=app%20commands#decorators
    """
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    @guild_only()
    @default_permissions()
    async def set_host_channel(self, interaction: discord.Interaction):
        """ Use this in the channel where submissions should be sent. """
        self.bot.config.host_channel_id = interaction.channel.id
        self.bot.update_config()
        await respond(interaction, 'Host channel set to this channel')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def set_submissions_message_channel(self, interaction: discord.Interaction):
        """ Use this in the channel where the current submissions message should be sent. """
        if self.bot.config.submissions_message.channel_id == interaction.channel.id:
            await respond(interaction, 'Submission message channel is already set to this channel')
            return

        self.bot.config.submissions_message.channel_id = interaction.channel.id
        self.bot.update_config()
        await respond(interaction, 'Submission message channel set to this channel')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def start_task(
            self,
            interaction: discord.Interaction,
            year: int,
            title: str,
            team_size: int,
    ):
        """ Create and start a new task. """
        if self.bot.config.host_channel_id is None:
            await respond(
                interaction,
                'Failed to create task: Host channel is not set. '
                'Use /set_host_channel in the channel where submissions should be sent.'
            )
            return

        self.bot.config.task = Task(
            year=year,
            title=title,
            team_size=team_size,
            is_accepting=True
        )
        self.bot.update_config()
        await respond(interaction, 'Created task and opened submissions.')


    @slash_command()
    @guild_only()
    @default_permissions()
    async def stop_task(self, interaction: discord.Interaction):
        """ Stop accepting submissions for the current task. """
        if not self.bot.config.task.is_accepting:
            await respond(interaction, 'Submissions are already closed.')
            return
        self.bot.config.task.is_accepting = False
        self.bot.update_config()
        await respond(interaction, 'Closed submissions for this task.')


    @slash_command(name='test')
    @guild_only()
    @default_permissions()
    async def say_hi(self, interaction: discord.Interaction):
        """ Test command """
        await respond(interaction, 'hi')
