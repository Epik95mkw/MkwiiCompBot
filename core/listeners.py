import io
import discord
from discord.ext.commands import Cog

from core.bot import Bot

MAX_FILE_SIZE = 50_000  # 50 KB

# Event reference: https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events

class Listeners(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener(name='on_message')
    async def handle_submission(self, message: discord.Message):
        if not isinstance(message.channel, discord.DMChannel) \
                or message.author == self.bot.user \
                or not message.attachments:
            return

        subm_guild = self.bot.get_guild(self.bot.config.guild_id)
        if subm_guild is None:
            await message.channel.send('Error: Bot does not have an active guild.')
            return

        subm_ch = subm_guild.get_channel(self.bot.config.host_channel_id)
        if subm_ch is None:
            await message.channel.send('Error: Bot is not configured to accept submissions.')
            return

        if not self.bot.config.task.is_accepting:
            await message.channel.send('Error: Bot is not currently accepting submissions.')
            return

        file = message.attachments[0]
        if file.size > MAX_FILE_SIZE:
            await message.channel.send(f'Submission failed: File must be {MAX_FILE_SIZE / 1000} KB or less.')
            return

        content = await file.read()
        if not content.startswith(b'RKGD'):
            await message.channel.send('Submission failed: File is not a valid RKG.')
            return

        username = message.author.name
        safe_title = ''.join(c for c in self.bot.config.task.title if c.isalnum())
        filename = f'{username}_{safe_title}_{self.bot.config.task.year}.rkg'
        bot_msg = await subm_ch.send(file=discord.File(io.BytesIO(content), filename=filename))
        self.bot.config.task.submissions[username] = bot_msg.id
        self.bot.update_config()
        await message.channel.send('Submission received.', file=discord.File(io.BytesIO(content), filename=filename))


    @Cog.listener(name='on_update_submission_message_channel')
    async def on_update_submission_message_channel(self, old_channel_id, new_channel_id):
        print('on_update_submission_message_channel')
        old_message_id = self.bot.config.submissions_message.message_id

        if old_channel_id is not None and old_message_id is not None:
            old_channel = self.bot.active_guild.get_channel(old_channel_id)
            if old_channel is not None:
                old_message = await old_channel.fetch_message(old_message_id)
                if old_message is not None:
                    await old_message.delete()

        new_channel = self.bot.active_guild.get_channel(new_channel_id)
        new_message = await new_channel.send(
            submission_message(self.bot.config.task.submissions)
        )
        self.bot.config.submissions_message.message_id = new_message.id
        self.bot.update_config()


    @Cog.listener(name='on_update_submissions')
    async def on_update_submissions(self, _, new_dict):
        print('on_update_submissions')
        channel_id = self.bot.config.submissions_message.channel_id
        message_id = self.bot.config.submissions_message.message_id

        channel = self.bot.active_guild.get_channel(channel_id or -1)
        if channel is not None:
            message = await channel.fetch_message(message_id or -1)
            if message is not None:
                await message.edit(content=submission_message(new_dict))
            else:
                await channel.send(content=submission_message(new_dict))


# HELPERS #

def submission_message(submissions: dict):
    return (
        '__**Current Submissions:**__\n' +
        '\n'.join(f'{i + 1}. {username}' for i, username in enumerate(submissions.keys()))
    )
