import io
import discord
from discord.ext.commands import Cog

from core.bot import Bot

# Event reference: https://discordpy.readthedocs.io/en/stable/api.html#discord-api-events

class Listeners(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if not isinstance(message.channel, discord.DMChannel) \
                or message.author == self.bot.user \
                or not message.attachments:
            return

        subm_ch = (
            self.bot
            .get_guild(self.bot.config.guild)
            .get_channel(self.bot.config.output_channel)
        )
        if subm_ch is None:
            await message.channel.send('Error: Bot is not configured to accept submissions.')
            return

        # TODO: if task is not currently running...

        file = message.attachments[0]
        if file.size > 50_000:
            await message.channel.send('Submission failed: File is too large.')
            return

        content = await file.read()
        if not content.startswith(b'RKGD'):
            await message.channel.send('Submission failed: File is not a valid RKG.')
            return

        username = message.author.name
        filename = f'{username}_task{self.bot.config.task.number}_{self.bot.config.task.year}'
        subm_file = discord.File(io.BytesIO(content), filename=filename)
        bot_msg = await subm_ch.send(f'{username}', file=subm_file)
        self.bot.config.task.submissions[username] = bot_msg.id
        self.bot.update_config()
        await message.channel.send('Submission received.', file=subm_file)
